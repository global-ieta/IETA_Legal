const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const root = document.documentElement;
if (!reduce) root.classList.add('motion-ready');

const splash = document.querySelector('#splash');
if (window.gsap && !reduce) {
  gsap.fromTo('.splash', { opacity: 1 }, { opacity: 0, duration: 0.6, delay: 0.55, onComplete: () => splash?.remove() });
  gsap.fromTo('.reveal', { autoAlpha: 0, y: 24 }, { autoAlpha: 1, y: 0, stagger: 0.09, duration: 0.8, delay: 0.35, ease: 'power3.out' });
} else {
  if (splash) splash.remove();
  document.querySelectorAll('.reveal').forEach((element) => { element.style.visibility = 'visible'; });
}

const scrollItems = document.querySelectorAll('[data-scroll-reveal]');
if (!reduce && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  }), { threshold: 0.16, rootMargin: '0px 0px -8%' });
  scrollItems.forEach((item) => observer.observe(item));
} else {
  scrollItems.forEach((item) => item.classList.add('is-visible'));
}

const visual = document.querySelector('[data-hero-visual]');
if (visual && !reduce && !window.matchMedia('(pointer: coarse)').matches) {
  visual.addEventListener('pointermove', (event) => {
    const bounds = visual.getBoundingClientRect();
    const x = ((event.clientX - bounds.left) / bounds.width - 0.5) * 12;
    const y = ((event.clientY - bounds.top) / bounds.height - 0.5) * 12;
    visual.style.setProperty('--pointer-x', `${x}px`);
    visual.style.setProperty('--pointer-y', `${y}px`);
  });
  visual.addEventListener('pointerleave', () => {
    visual.style.setProperty('--pointer-x', '0px');
    visual.style.setProperty('--pointer-y', '0px');
  });
}

const toggle = document.querySelector('[data-mobile-toggle]');
const nav = document.querySelector('[data-mobile-nav]');
if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
}
