// Keep previously shared hash routes working while using crawlable page URLs.
const legacy = location.hash.match(/^#\/(home|offer|thinking)(?:\/([^/?#]+))?$/);
if (legacy) {
 const paths = {home: '/', offer: '/what-i-offer/', thinking: '/how-i-think/'};
 location.replace(paths[legacy[1]] + (legacy[2] ? '#' + legacy[2] : ''));
}
const menu=document.querySelector('.mobile-menu'),nav=document.querySelector('nav');
if(menu)menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));menu.textContent=open?'Close':'Menu';nav.classList.toggle('open',open)});

const tabs=[...document.querySelectorAll('[role="tab"]')];
 function activate(t){tabs.forEach(x=>{const active=x===t;x.setAttribute('aria-selected',String(active));x.tabIndex=active?0:-1;document.getElementById(x.getAttribute('aria-controls')).hidden=!active})}
 tabs.forEach((t,i)=>{t.addEventListener('click',()=>activate(t));t.addEventListener('keydown',e=>{let n;if(['ArrowDown','ArrowRight'].includes(e.key))n=(i+1)%tabs.length;if(['ArrowUp','ArrowLeft'].includes(e.key))n=(i+tabs.length-1)%tabs.length;if(e.key==='Home')n=0;if(e.key==='End')n=tabs.length-1;if(n!==undefined){e.preventDefault();activate(tabs[n]);tabs[n].focus()}})});
 const copy=document.getElementById('copy-email');if(copy)copy.addEventListener('click',async()=>{try{await navigator.clipboard.writeText('brandi@mestamedia.com');document.getElementById('copy-status').textContent='Email address copied.'}catch{document.getElementById('copy-status').textContent='brandi@mestamedia.com'}});
 document.querySelectorAll('.reveal').forEach(x=>x.classList.add('visible'));

