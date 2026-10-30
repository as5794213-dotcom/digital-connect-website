// Mobile menu
const burger=document.querySelector('.burger'),menu=document.querySelector('.menu');
if(burger){burger.addEventListener('click',()=>{const o=menu.classList.toggle('open');burger.setAttribute('aria-expanded',o)});}
document.querySelectorAll('.has-sub>a').forEach(a=>a.addEventListener('click',e=>{if(window.innerWidth<=900){e.preventDefault();a.parentElement.classList.toggle('open-sub')}}));

// Reveal on scroll + counters
const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;e.target.classList.add('in');
  e.target.querySelectorAll('[data-count]').forEach(el=>{const end=parseFloat(el.dataset.count),dec=(el.dataset.count.split('.')[1]||'').length,suf=el.dataset.suffix||'';let t0=null;
    const step=t=>{t0=t0||t;const p=Math.min((t-t0)/1400,1);el.textContent=(end*(1-Math.pow(1-p,3))).toFixed(dec)+suf;if(p<1)requestAnimationFrame(step)};requestAnimationFrame(step)});
  io.unobserve(e.target)}),{threshold:.15});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

// Lead form -> also opens WhatsApp with the details (Netlify Forms stores the submission)
document.querySelectorAll('form[data-wa]').forEach(f=>f.addEventListener('submit',e=>{
  const d=new FormData(f);
  const msg=`Hi Digital Connect, I'd like a free growth plan.%0AName: ${d.get('name')||''}%0APhone: ${d.get('phone')||''}%0ABusiness: ${d.get('business')||''}%0AService: ${d.get('service')||''}%0A${d.get('message')||''}`;
  try{sessionStorage.setItem('dc_wa',msg)}catch(_){}
}));
const yr=document.getElementById('yr');if(yr)yr.textContent=new Date().getFullYear();
