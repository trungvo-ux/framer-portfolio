/* Minimal portfolio — motion controller
   - line-mask hero reveal on load
   - IntersectionObserver scroll reveals (one-shot)
   - sticky header hairline on scroll
   - reading progress bar (case study)
   All of it defers to prefers-reduced-motion via CSS; the JS below only
   toggles classes, so reduced-motion users get instant, static content. */

(() => {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- load reveal: arms the hero line masks ---- */
  document.documentElement.classList.add("is-loaded");

  /* ---- scroll reveals ---- */
  const revealables = document.querySelectorAll("[data-reveal]");

  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealables.forEach((el) => el.classList.add("is-visible"));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        }
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );
    revealables.forEach((el) => io.observe(el));
  }

  /* ---- header hairline + reading progress, one rAF-throttled pass ---- */
  const header = document.querySelector("[data-header]");
  const progress = document.querySelector("[data-progress]");
  let ticking = false;

  const update = () => {
    ticking = false;
    const y = window.scrollY;

    if (header) header.classList.toggle("is-scrolled", y > 8);

    if (progress) {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = `scaleX(${max > 0 ? Math.min(y / max, 1) : 0})`;
    }
  };

  window.addEventListener(
    "scroll",
    () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    },
    { passive: true }
  );

  update();
})();
