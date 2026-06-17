const currentYear = document.querySelector("#current-year");

if (currentYear) {
  currentYear.textContent = new Date().getFullYear();
}

const revealItems = document.querySelectorAll("[data-reveal]");

if ("IntersectionObserver" in window && revealItems.length > 0) {
  const observer = new IntersectionObserver(
    (entries, activeObserver) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        entry.target.classList.add("is-visible");
        activeObserver.unobserve(entry.target);
      });
    },
    {
      threshold: 0.18,
      rootMargin: "0px 0px -40px 0px",
    },
  );

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

// ---- Formspree AJAX submission ----
function bindEstimateForm(form) {
  if (!form || form.dataset.bound === "true") return;
  const success =
    document.getElementById(`${form.id}-success`) ||
    form.parentElement.querySelector(".form-success");
  if (!success) return;

  form.dataset.bound = "true";
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const submitBtn = form.querySelector("[type='submit']");
    const originalText = submitBtn.textContent;

    submitBtn.disabled = true;
    submitBtn.textContent = "Sending...";

    try {
      const res = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" },
      });

      let data = null;
      try {
        data = await res.json();
      } catch {
        data = null;
      }

      if (res.ok) {
        submitBtn.textContent = "Sent!";
        if (typeof gtag === "function") {
          gtag("event", "generate_lead", { event_category: "form", event_label: form.id || "estimate_form" });
        }
        setTimeout(() => {
          form.hidden = true;
          success.hidden = false;
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
        }, 1800);
      } else {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
        const msg =
          (data && (data.error || data.message)) ||
          "Something went wrong. Please email contact@faithworksods.com directly.";
        alert(msg);
      }
    } catch {
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
      alert("Could not send. Please email contact@faithworksods.com directly.");
    }
  });
}

document.querySelectorAll(".contact-form").forEach(bindEstimateForm);

document.querySelectorAll('a[href^="tel:"]').forEach((link) => {
  link.addEventListener("click", () => {
    if (typeof gtag === "function") {
      gtag("event", "phone_click", { event_category: "contact", event_label: link.getAttribute("href") });
    }
  });
});

// ---- Services nav dropdown ----
const dropdownBtn  = document.querySelector('.nav-dropdown-btn');
const dropdownMenu = document.querySelector('.nav-dropdown-menu');

if (dropdownBtn && dropdownMenu) {
  dropdownBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const expanded = dropdownBtn.getAttribute('aria-expanded') === 'true';
    dropdownBtn.setAttribute('aria-expanded', String(!expanded));
  });

  dropdownMenu.addEventListener('click', (e) => e.stopPropagation());

  document.addEventListener('click', () => {
    dropdownBtn.setAttribute('aria-expanded', 'false');
  });
}

// ---- FAQ accordion ----
document.querySelectorAll('.faq-question').forEach((btn) => {
  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    const answer   = document.getElementById(btn.getAttribute('aria-controls'));

    // Close all others
    document.querySelectorAll('.faq-question').forEach((otherBtn) => {
      const otherAnswer = document.getElementById(otherBtn.getAttribute('aria-controls'));
      otherBtn.setAttribute('aria-expanded', 'false');
      if (otherAnswer) {
        otherAnswer.setAttribute('aria-hidden', 'true');
        otherAnswer.setAttribute('inert', '');
      }
    });

    // Toggle clicked
    btn.setAttribute('aria-expanded', String(!expanded));
    if (answer) {
      answer.setAttribute('aria-hidden', String(expanded));
      if (expanded) { answer.setAttribute('inert', ''); } else { answer.removeAttribute('inert'); }
    }
  });
});

// ---- Hamburger mobile nav ----
const hamburgerBtn     = document.getElementById('hamburger-btn');
const mobileNav        = document.getElementById('mobile-nav');
const navOverlay       = document.getElementById('nav-overlay');
const mobileNavClose   = document.getElementById('mobile-nav-close');
const mobileServToggle = document.getElementById('mobile-services-toggle');
const mobileServicesSub = document.getElementById('mobile-services-sub');

function openMobileNav() {
  mobileNav.classList.add('is-open');
  navOverlay.classList.add('is-open');
  hamburgerBtn.classList.add('is-open');
  hamburgerBtn.setAttribute('aria-expanded', 'true');
  mobileNav.setAttribute('aria-hidden', 'false');
  mobileNav.removeAttribute('inert');
  document.body.style.overflow = 'hidden';
}

function closeMobileNav() {
  mobileNav.classList.remove('is-open');
  navOverlay.classList.remove('is-open');
  hamburgerBtn.classList.remove('is-open');
  hamburgerBtn.setAttribute('aria-expanded', 'false');
  mobileNav.setAttribute('aria-hidden', 'true');
  mobileNav.setAttribute('inert', '');
  document.body.style.overflow = '';
}

if (hamburgerBtn) {
  hamburgerBtn.addEventListener('click', () => {
    hamburgerBtn.classList.contains('is-open') ? closeMobileNav() : openMobileNav();
  });
}
if (mobileNavClose) mobileNavClose.addEventListener('click', closeMobileNav);
if (navOverlay)     navOverlay.addEventListener('click', closeMobileNav);

// Close mobile nav when a link is tapped
if (mobileNav) {
  mobileNav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeMobileNav);
  });
}

// Close mobile nav on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && mobileNav && mobileNav.classList.contains('is-open')) {
    closeMobileNav();
  }
});

// Services sub-menu accordion in mobile drawer
if (mobileServToggle && mobileServicesSub) {
  mobileServToggle.addEventListener('click', () => {
    const open = mobileServToggle.classList.toggle('is-open');
    mobileServicesSub.classList.toggle('is-open', open);
    mobileServToggle.setAttribute('aria-expanded', String(open));
  });
}
// ---- Hero parallax ----
(function initHeroParallax() {
  const hero = document.querySelector(".hero");
  const bg = hero && hero.querySelector(".hero-bg");
  if (!hero || !bg) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  let restTop = 0;
  let ticking = false;
  const rate = 0.45;

  function update() {
    ticking = false;
    const rect = hero.getBoundingClientRect();
    if (window.scrollY < 2) {
      const header = document.querySelector(".site-header");
      restTop = header ? header.getBoundingClientRect().height : rect.top;
    }
    const shift = -(rect.top - restTop) * rate;
    bg.style.setProperty("--hero-shift", Math.round(shift) + "px");
  }

  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  update();
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", queue, { passive: true });
})();
