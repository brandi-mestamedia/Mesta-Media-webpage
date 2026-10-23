"""Validate the rendered site, rather than just the source templates."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json, sys, xml.etree.ElementTree as ET

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []; self.headings = []; self.ids = []; self.jsonld = []
        self.active_json = None; self.in_main = False; self.main_text = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs); self.tags.append((tag, attrs))
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag in ['h1','h2','h3','h4','h5','h6']: self.headings.append(int(tag[1]))
        if tag == 'main': self.in_main = True
        if tag == 'script' and attrs.get('type') == 'application/ld+json': self.active_json = ''
    def handle_endtag(self, tag):
        if tag == 'main': self.in_main = False
        if tag == 'script' and self.active_json is not None:
            self.jsonld.append(json.loads(self.active_json)); self.active_json = None
    def handle_data(self, text):
        if self.active_json is not None: self.active_json += text
        if self.in_main: self.main_text.append(text)

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
routes = ['/', '/what-i-offer/', '/how-i-think/']
pages = {}
for route in routes:
    path = root / route.lstrip('/') / 'index.html'
    text = path.read_text(); p = Page(text); pages[route] = p
    assert '{{' not in text and '{%' not in text, f'Unrendered Liquid: {route}'
    assert p.headings.count(1) == 1 and p.headings[0] == 1, f'H1: {route}'
    assert all(b <= a+1 for a,b in zip(p.headings,p.headings[1:])), f'Heading jump: {route}'
    assert len(p.ids) == len(set(p.ids)), f'Duplicate IDs: {route}'
    assert len(' '.join(p.main_text).strip()) > 1500, f'Missing static content: {route}'
    assert sum(t == 'main' for t,a in p.tags) == 1
    assert sum(t == 'title' for t,a in p.tags) == 1
    metas = [a for t,a in p.tags if t == 'meta']
    for key, value in [('name','description'),('property','og:title'),('property','og:description'),('property','og:url'),('property','og:image'),('property','og:image:alt'),('name','twitter:card')]:
        match = [a for a in metas if a.get(key) == value]
        assert len(match) == 1 and match[0].get('content'), f'{route}: {value}'
    canonical = [a for t,a in p.tags if t == 'link' and a.get('rel') == 'canonical']
    assert len(canonical) == 1 and canonical[0]['href'] == 'https://mestamedia.com'+route
    assert len(p.jsonld) == 1, f'Expected one JSON-LD graph: {route}'
    graph = p.jsonld[0]['@graph']; ids = [x['@id'] for x in graph]
    assert len(ids) == len(set(ids))
    assert {'Organization','Person','WebSite','WebPage'} <= {x['@type'] for x in graph}
    if route == '/what-i-offer/': assert sum(x['@type']=='Service' for x in graph) == 4
    for t,a in p.tags:
        if t == 'img': assert 'alt' in a
    mirror = root / route.lstrip('/') / 'index.html.md'
    assert mirror.exists() and mirror.read_text().startswith('# ')

for route,p in pages.items():
    for tag,a in p.tags:
        for attr in ['href','src']:
            value = a.get(attr,''); u = urlsplit(value)
            if u.scheme and u.netloc != 'mestamedia.com': continue
            if u.scheme in ['mailto','tel','data']: continue
            if not value or not u.path.startswith('/'): continue
            target = root / unquote(u.path.lstrip('/'))
            if u.path.endswith('/'): target = target / 'index.html'
            assert target.exists(), f'{route}: missing {value}'
            if u.fragment and target.suffix == '.html':
                assert u.fragment in Page(target.read_text()).ids, f'Missing anchor: {value}'
    for _,a in [x for x in p.tags if x[0]=='meta' and x[1].get('property')=='og:image']:
        assert (root / urlsplit(a['content']).path.lstrip('/')).is_file()

assert (root/'robots.txt').read_text().startswith('User-agent: *')
assert 'Sitemap: https://mestamedia.com/sitemap.xml' in (root/'robots.txt').read_text()
ET.parse(root/'sitemap.xml')
assert (root/'llms.txt').read_text().startswith('# Mesta Media')
assert (root/'CNAME').read_text().strip() == 'mestamedia.com'
print('PASS: three crawlable pages, heading hierarchy, metadata, single linked JSON-LD graphs, internal links, Markdown, sitemap, robots and llms.txt.')
