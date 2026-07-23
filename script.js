const currentYear = document.querySelector("#current-year");

if (currentYear) {
  currentYear.textContent = new Date().getFullYear();
}

document.documentElement.classList.add("fw-js");

function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function tagSpHeroEnters() {
  document.querySelectorAll(".sp-hero .container").forEach((container) => {
    const eyebrow = container.querySelector(".eyebrow");
    const h1 = container.querySelector("h1");
    const lead = container.querySelector("p:not(.eyebrow)");
    if (eyebrow && !eyebrow.hasAttribute("data-fw-enter")) {
      eyebrow.setAttribute("data-fw-enter", "left");
      eyebrow.setAttribute("data-fw-enter-immediate", "true");
    }
    if (h1 && !h1.hasAttribute("data-fw-enter")) {
      h1.setAttribute("data-fw-enter", "left");
      h1.setAttribute("data-fw-enter-immediate", "true");
      h1.style.setProperty("--fw-enter-delay", "80ms");
    }
    if (lead && !lead.hasAttribute("data-fw-enter")) {
      lead.setAttribute("data-fw-enter", "left");
      lead.setAttribute("data-fw-enter-immediate", "true");
      lead.style.setProperty("--fw-enter-delay", "160ms");
    }
  });
}

function initEnterAnimations() {
  tagSpHeroEnters();
  const items = document.querySelectorAll("[data-fw-enter]");
  if (prefersReducedMotion()) {
    items.forEach((el) => el.classList.add("is-visible"));
    return;
  }
  document.querySelectorAll('[data-fw-enter-immediate="true"]').forEach((el) => {
    el.classList.add("is-visible");
  });
  if (!("IntersectionObserver" in window)) {
    items.forEach((el) => el.classList.add("is-visible"));
    return;
  }
  const observer = new IntersectionObserver(
    (entries, activeObserver) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        activeObserver.unobserve(entry.target);
      });
    },
    { rootMargin: "0px 0px -10% 0px", threshold: 0.12 },
  );
  document
    .querySelectorAll('[data-fw-enter]:not([data-fw-enter-immediate="true"]):not(.is-visible)')
    .forEach((el) => observer.observe(el));
}

initEnterAnimations();

(function initContactCutout() {
  const section = document.querySelector(".contact-section");
  if (!section || !section.querySelector(".contact-cutout")) return;

  if (prefersReducedMotion()) {
    section.classList.add("contact-ready");
    return;
  }

  if (!("IntersectionObserver" in window)) {
    section.classList.add("contact-ready");
    return;
  }

  const observer = new IntersectionObserver(
    (entries, activeObserver) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        section.classList.add("contact-ready");
        activeObserver.unobserve(section);
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.12 },
  );
  observer.observe(section);
})();

// ---- Formspree AJAX submission ----
function currentUtmParams() {
  const params = new URLSearchParams(window.location.search);
  const keys = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"];
  return keys.reduce((acc, key) => {
    acc[key] = params.get(key) || "";
    return acc;
  }, {});
}

function setHiddenValue(form, name, value) {
  const field = form.querySelector(`input[type="hidden"][name="${name}"]`);
  if (field) field.value = value || "";
}

function populateLeadAttribution(form) {
  const utms = currentUtmParams();
  setHiddenValue(form, "page_url", window.location.href);
  setHiddenValue(form, "page_title", document.title);
  setHiddenValue(form, "referrer", document.referrer);
  Object.entries(utms).forEach(([key, value]) => setHiddenValue(form, key, value));
}

function trackConversionEvent(eventName, params = {}) {
  if (typeof gtag !== "function") return;
  gtag("event", eventName, {
    page_location: window.location.href,
    page_title: document.title,
    ...params,
  });
}

function validateEstimateForm(form) {
  const gotcha = form.querySelector('input[name="_gotcha"]');
  if (gotcha && gotcha.value.trim()) {
    return "bot";
  }

  form.querySelectorAll("input:not([type='hidden']), textarea, select").forEach((field) => {
    if (typeof field.value === "string") {
      field.value = field.value.trim();
    }
    field.setCustomValidity("");
  });

  const name = form.querySelector('input[name="name"]');
  if (name && name.value.length < 2) {
    name.setCustomValidity("Please enter your name.");
    name.reportValidity();
    return false;
  }

  const phone = form.querySelector('input[name="phone"]');
  if (phone) {
    const digits = phone.value.replace(/\D/g, "");
    if (digits.length < 10) {
      phone.setCustomValidity("Please enter a valid 10-digit phone number.");
      phone.reportValidity();
      return false;
    }
  }

  const service = form.querySelector('select[name="service"]');
  if (service && !service.value.trim()) {
    service.setCustomValidity("Please select a service.");
    service.reportValidity();
    return false;
  }

  const message = form.querySelector('textarea[name="message"]');
  if (message && message.value.length < 5) {
    message.setCustomValidity("Please describe what you need (at least a few words).");
    message.reportValidity();
    return false;
  }

  if (!form.checkValidity()) {
    form.reportValidity();
    return false;
  }

  return true;
}

function bindEstimateForm(form) {
  if (!form || form.dataset.bound === "true") return;
  if (form.dataset.formMode === "email" || form.action.startsWith("mailto:")) return;
  // FormSubmit uses a normal browser POST so the first submission can trigger activation email delivery.
  if (form.dataset.formMode === "formsubmit") return;
  const success =
    document.getElementById(`${form.id}-success`) ||
    form.parentElement.querySelector(".form-success");
  if (!success) return;

  form.dataset.bound = "true";
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const validation = validateEstimateForm(form);
    if (validation === "bot") {
      form.hidden = true;
      success.hidden = false;
      return;
    }
    if (!validation) return;

    const submitBtn = form.querySelector("[type='submit']");
    const originalText = submitBtn.textContent;

    populateLeadAttribution(form);
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
        trackConversionEvent("generate_lead", {
          event_category: "form",
          event_label: form.id || "estimate_form",
          form_id: form.id || "",
          service: (form.querySelector('[name="service"]') && form.querySelector('[name="service"]').value) || "",
          form_page: (form.querySelector('[name="page"]') && form.querySelector('[name="page"]').value) || "",
        });
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
          "Something went wrong. Please email tyler@faithworksclearing.com directly.";
        alert(msg);
      }
    } catch {
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
      alert("Could not send. Please email tyler@faithworksclearing.com directly.");
    }
  });
}

document.querySelectorAll(".contact-form").forEach(bindEstimateForm);

document.querySelectorAll('a[href^="tel:"]').forEach((link) => {
  link.addEventListener("click", () => {
    trackConversionEvent("phone_click", {
      event_category: "contact",
      event_label: link.getAttribute("href"),
      link_text: link.textContent.trim().replace(/\s+/g, " "),
      cta_location: link.closest("header")
        ? "header"
        : link.closest("footer")
          ? "footer"
          : link.closest("aside")
            ? "sidebar"
            : "body",
    });
  });
});

// ---- Nav mega menus (desktop flyout + mobile accordion) ----
(function initNavMegaMenus() {
  const HOVER_CLOSE_DELAY = 220;
  const MQ_DESKTOP = window.matchMedia("(min-width: 1201px)");

  function closeDesktopBranches(menu, except) {
    if (!menu) return;
    menu.querySelectorAll(".fw-services-mega__item--branch.subnav-open").forEach((item) => {
      if (item === except) return;
      item.classList.remove("subnav-open");
      const btn = item.querySelector(".subnav-toggle");
      const flyout = item.querySelector(".fw-services-mega__flyout");
      if (btn) btn.setAttribute("aria-expanded", "false");
      if (flyout) {
        item.classList.remove("is-flyout-left");
        flyout.classList.remove("is-open-left");
      }
    });
  }

  function placeMenu(wrap) {
    if (!MQ_DESKTOP.matches) return;
    const btn = wrap.querySelector(".nav-dropdown-btn");
    const menu = wrap.querySelector(".nav-dropdown-menu");
    if (!btn || !menu) return;

    const rect = btn.getBoundingClientRect();
    const header = document.querySelector('.site-header');
    const headerBottom = header ? header.getBoundingClientRect().bottom : rect.bottom;
    const gap = 8;
    const menuWidth = Math.max(menu.offsetWidth || 272, 272);
    let left = rect.left + rect.width / 2 - menuWidth * 0.58;
    left = Math.max(12, Math.min(left, window.innerWidth - menuWidth - 12));
    // Sit just under the sticky header so the panel never overlaps nav text
    const top = Math.min(Math.max(rect.bottom + gap, headerBottom + 4), window.innerHeight - 24);

    menu.style.setProperty("--fw-menu-top", Math.round(top) + "px");
    menu.style.setProperty("--fw-menu-left", Math.round(left) + "px");
  }

  function placeFlyout(item) {
    if (!MQ_DESKTOP.matches) return;
    const flyout = item.querySelector(".fw-services-mega__flyout");
    if (!flyout) return;

    const rect = item.getBoundingClientRect();
    const approxWidth = Math.max(flyout.offsetWidth || 252, 252);
    const openLeft = rect.right + 8 + approxWidth > window.innerWidth - 12;
    item.classList.toggle("is-flyout-left", openLeft);
    flyout.classList.toggle("is-open-left", openLeft);
  }

  function setDropdownOpen(wrap, open) {
    const dropdownBtn = wrap.querySelector(".nav-dropdown-btn");
    const dropdownMenu = wrap.querySelector(".nav-dropdown-menu");
    if (!dropdownBtn || !dropdownMenu) return;
    dropdownBtn.setAttribute("aria-expanded", String(open));
    wrap.classList.toggle("is-open", open);
    if (open) {
      placeMenu(wrap);
    } else {
      closeDesktopBranches(dropdownMenu);
      dropdownMenu.style.removeProperty("--fw-menu-top");
      dropdownMenu.style.removeProperty("--fw-menu-left");
    }
  }

  function closeAllDesktopDropdowns(exceptWrap) {
    document.querySelectorAll(".nav-dropdown-wrap").forEach((wrap) => {
      if (wrap === exceptWrap) return;
      setDropdownOpen(wrap, false);
    });
  }

  function repositionOpenMenus() {
    document.querySelectorAll(".nav-dropdown-wrap.is-open").forEach((wrap) => {
      placeMenu(wrap);
      wrap.querySelectorAll(".fw-services-mega__item--branch.subnav-open").forEach((item) => {
        placeFlyout(item);
      });
    });
  }

  document.querySelectorAll(".nav-dropdown-wrap").forEach((wrap) => {
    const dropdownBtn = wrap.querySelector(".nav-dropdown-btn");
    const dropdownMenu = wrap.querySelector(".nav-dropdown-menu");
    if (!dropdownBtn || !dropdownMenu) return;

    let closeTimer = null;

    const cancelClose = () => {
      if (closeTimer) {
        clearTimeout(closeTimer);
        closeTimer = null;
      }
    };

    const scheduleClose = () => {
      cancelClose();
      closeTimer = setTimeout(() => setDropdownOpen(wrap, false), HOVER_CLOSE_DELAY);
    };

    const openDropdown = () => {
      if (!MQ_DESKTOP.matches) return;
      cancelClose();
      closeAllDesktopDropdowns(wrap);
      setDropdownOpen(wrap, true);
    };

    wrap.addEventListener("mouseenter", openDropdown);
    wrap.addEventListener("mouseleave", scheduleClose);
    dropdownMenu.addEventListener("mouseenter", cancelClose);
    dropdownMenu.addEventListener("mouseleave", scheduleClose);
    wrap.addEventListener("focusin", openDropdown);
    wrap.addEventListener("focusout", (e) => {
      if (!wrap.contains(e.relatedTarget) && !dropdownMenu.contains(e.relatedTarget)) {
        scheduleClose();
      }
    });

    dropdownMenu.querySelectorAll(".fw-services-mega__item--branch").forEach((item) => {
      const btn = item.querySelector(".subnav-toggle");
      if (!btn) return;

      let branchTimer = null;

      const openBranch = () => {
        if (branchTimer) clearTimeout(branchTimer);
        closeDesktopBranches(dropdownMenu, item);
        item.classList.add("subnav-open");
        btn.setAttribute("aria-expanded", "true");
        requestAnimationFrame(() => placeFlyout(item));
      };

      const scheduleBranchClose = () => {
        if (branchTimer) clearTimeout(branchTimer);
        branchTimer = setTimeout(() => {
          if (!item.matches(":hover") && !item.contains(document.activeElement)) {
            item.classList.remove("subnav-open");
            btn.setAttribute("aria-expanded", "false");
          }
        }, HOVER_CLOSE_DELAY);
      };

      item.addEventListener("mouseenter", openBranch);
      item.addEventListener("mouseleave", scheduleBranchClose);
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        const opening = !item.classList.contains("subnav-open");
        closeDesktopBranches(dropdownMenu, opening ? item : null);
        item.classList.toggle("subnav-open", opening);
        btn.setAttribute("aria-expanded", String(opening));
        if (opening) requestAnimationFrame(() => placeFlyout(item));
      });
    });

    dropdownBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      if (!MQ_DESKTOP.matches) return;
      const expanded = dropdownBtn.getAttribute("aria-expanded") === "true";
      if (expanded) setDropdownOpen(wrap, false);
      else openDropdown();
    });

    dropdownMenu.addEventListener("click", (e) => e.stopPropagation());
  });

  document.addEventListener("click", () => closeAllDesktopDropdowns());
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeAllDesktopDropdowns();
  });
  window.addEventListener("scroll", repositionOpenMenus, { passive: true });
  window.addEventListener("resize", () => {
    if (!MQ_DESKTOP.matches) closeAllDesktopDropdowns();
    else repositionOpenMenus();
  });

  function resetMobileBranches() {
    document.querySelectorAll(".fw-mm-item--branch.fw-mm-item--open").forEach((item) => {
      item.classList.remove("fw-mm-item--open");
      const btn = item.querySelector(".fw-mm-trigger");
      const submenu = item.querySelector(".fw-mm-submenu");
      if (btn) btn.setAttribute("aria-expanded", "false");
      if (submenu) submenu.hidden = true;
    });
  }

  document.querySelectorAll(".fw-mm-item--branch > .fw-mm-trigger").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      const item = btn.closest(".fw-mm-item--branch");
      const submenu = document.getElementById(btn.getAttribute("aria-controls"));
      if (!item) return;
      const opening = !item.classList.contains("fw-mm-item--open");
      const parent = item.parentElement;
      if (parent) {
        parent.querySelectorAll(":scope > .fw-mm-item--branch.fw-mm-item--open").forEach((other) => {
          if (other === item) return;
          other.classList.remove("fw-mm-item--open");
          const otherBtn = other.querySelector(".fw-mm-trigger");
          const otherSub = other.querySelector(".fw-mm-submenu");
          if (otherBtn) otherBtn.setAttribute("aria-expanded", "false");
          if (otherSub) otherSub.hidden = true;
        });
      }
      item.classList.toggle("fw-mm-item--open", opening);
      btn.setAttribute("aria-expanded", String(opening));
      if (submenu) submenu.hidden = !opening;
    });
  });

  window.resetFaithWorksMobileSubmenus = resetMobileBranches;
})();

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
  if (typeof window.resetFaithWorksMobileSubmenus === "function") {
    window.resetFaithWorksMobileSubmenus();
  }
  document.querySelectorAll(".mobile-services-toggle.is-open").forEach((toggle) => {
    toggle.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    const sub = document.getElementById(toggle.getAttribute("aria-controls"));
    if (sub) sub.classList.remove("is-open");
  });
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

// Mobile drawer sub-menus (Service Menu + Service Areas)
document.querySelectorAll(".mobile-services-toggle").forEach((toggle) => {
  const subId = toggle.getAttribute("aria-controls");
  const sub = subId ? document.getElementById(subId) : null;
  if (!sub) return;
  toggle.addEventListener("click", () => {
    const open = toggle.classList.toggle("is-open");
    sub.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
  });
});
// ---- Reviews carousel (GBP-backed via data/google-reviews.json) ----
(function initFaithWorksReviews() {
  const carousels = document.querySelectorAll("[data-fw-review-carousel]");
  if (!carousels.length) return;

  carousels.forEach((carousel) => {
    const track = carousel.querySelector("#fw-review-track") || carousel.querySelector(".fw-review-track");
    const prev = document.getElementById("fw-review-prev") || carousel.querySelector(".fw-review-btn:first-of-type");
    const next = document.getElementById("fw-review-next") || carousel.querySelector(".fw-review-btn:last-of-type");
    const showcase = carousel.closest(".fw-reviews-showcase");
    const dotsWrap = document.getElementById("fw-review-dots") || (showcase && showcase.querySelector(".fw-review-dots"));
    const summaryEl = document.getElementById("fw-review-summary");
    const starsEl = document.getElementById("fw-review-stars");
    const mapRatingEl = document.getElementById("fw-map-rating");
    const seedEl = showcase ? showcase.querySelector("#google-reviews-seed") : null;

    if (!track || !prev || !next || !dotsWrap || !showcase) return;

    let cards = [];
    let currentIndex = 0;
    let reviews = [];

    function escapeHtml(value) {
      return String(value || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    }

    function getInitial(name) {
      const clean = String(name || "").trim();
      return clean ? clean.charAt(0).toUpperCase() : "?";
    }

    function formatStars(count) {
      const stars = Math.max(1, Math.min(5, Number(count) || 5));
      return "\u2605".repeat(stars);
    }

    function reviewCardMarkup(review) {
      return (
        '<article class="fw-review-card">' +
        '<div class="fw-review-header">' +
        '<span class="fw-review-avatar" style="background:' +
        escapeHtml(review.avatarColor || "#c9a227") +
        ';" aria-hidden="true">' +
        escapeHtml(getInitial(review.name)) +
        "</span>" +
        "<div>" +
        '<p class="fw-review-name">' +
        escapeHtml(review.name) +
        "</p>" +
        '<div class="fw-review-sub">' +
        escapeHtml(review.meta || "Google review") +
        "</div>" +
        "</div>" +
        "</div>" +
        '<div class="fw-review-stars" role="img" aria-label="' +
        escapeHtml(String(Number(review.stars) || 5)) +
        ' stars">' +
        formatStars(review.stars) +
        "</div>" +
        '<p class="fw-review-text">' +
        escapeHtml(review.text || "") +
        "</p>" +
        '<div class="fw-review-date">' +
        escapeHtml(review.date || "") +
        "</div>" +
        "</article>"
      );
    }

    function applySummary(payload) {
      const ratingNum = Number(payload.ratingValue || 5);
      const rating = ratingNum.toFixed(1);
      const count = Number(payload.reviewCount || reviews.length || 0);
      const roundedStars = Math.max(1, Math.min(5, Math.round(ratingNum)));
      const label = count === 1 ? " review" : " reviews";
      if (summaryEl) summaryEl.textContent = rating + " \u00b7 " + count + label;
      if (starsEl) {
        starsEl.textContent = formatStars(roundedStars);
        starsEl.setAttribute("aria-label", rating + " out of 5 stars");
      }
      if (mapRatingEl) {
        mapRatingEl.textContent =
          formatStars(roundedStars) + " " + rating + " \u00b7 " + count + " Google review" + (count === 1 ? "" : "s");
        mapRatingEl.setAttribute(
          "aria-label",
          rating + " out of 5 stars, " + count + " Google reviews",
        );
      }
    }

    function perView() {
      if (window.innerWidth < 720) return 1;
      if (window.innerWidth < 1060) return 2;
      return 3;
    }

    function pageCount() {
      return Math.max(1, Math.ceil(cards.length / perView()));
    }

    function maxIndex() {
      return Math.max(0, cards.length - perView());
    }

    function cardSpan() {
      if (!cards.length) return 0;
      const styles = window.getComputedStyle(track);
      const gap = parseFloat(styles.columnGap || styles.gap || "18");
      return cards[0].getBoundingClientRect().width + gap;
    }

    function updateButtons() {
      const singlePage = pageCount() <= 1 || cards.length === 0;
      prev.disabled = singlePage || currentIndex <= 0;
      next.disabled = singlePage || currentIndex >= maxIndex();
    }

    function update() {
      currentIndex = Math.max(0, Math.min(currentIndex, maxIndex()));
      track.style.transform = "translateX(" + -currentIndex * cardSpan() + "px)";
      const activePage = Math.floor(currentIndex / perView());
      Array.from(dotsWrap.children).forEach((dot, dotIndex) => {
        const isActive = dotIndex === activePage;
        dot.classList.toggle("is-active", isActive);
        if (isActive) dot.setAttribute("aria-current", "true");
        else dot.removeAttribute("aria-current");
      });
      updateButtons();
    }

    function renderDots() {
      dotsWrap.innerHTML = "";
      for (let i = 0; i < pageCount(); i += 1) {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "fw-review-dot" + (i === 0 ? " is-active" : "");
        dot.setAttribute("aria-label", "Go to review page " + (i + 1));
        if (i === 0) dot.setAttribute("aria-current", "true");
        dot.addEventListener("click", () => {
          currentIndex = i * perView();
          update();
        });
        dotsWrap.appendChild(dot);
      }
    }

    function renderReviews(payload) {
      reviews = Array.isArray(payload.reviews) ? payload.reviews.slice() : [];
      applySummary(payload);

      if (!reviews.length) {
        track.innerHTML =
          '<article class="fw-review-card"><p class="fw-review-text">Reviews will appear here once posted on Google.</p></article>';
      } else {
        track.innerHTML = reviews.map(reviewCardMarkup).join("");
      }

      cards = Array.from(track.querySelectorAll(".fw-review-card"));
      currentIndex = 0;
      renderDots();
      update();
    }

    function parseSeedPayload() {
      if (!seedEl) return null;
      try {
        return JSON.parse(seedEl.textContent || "{}");
      } catch (error) {
        console.warn("Google review seed parse failed:", error);
        return null;
      }
    }

    function reviewsFeedUrl() {
      const script = document.querySelector('script[src*="script.js"]');
      if (script && script.src) {
        return new URL("data/google-reviews.json", script.src).href;
      }
      return new URL("data/google-reviews.json", window.location.href).href;
    }

    async function loadReviews() {
      let payload = null;
      try {
        const response = await fetch(reviewsFeedUrl(), { cache: "no-store" });
        if (response.ok) payload = await response.json();
      } catch (error) {
        console.warn("Google review feed fetch failed, using seed data:", error);
      }

      if (!payload) payload = parseSeedPayload();
      if (!payload || !Array.isArray(payload.reviews)) {
        payload = { ratingValue: 5, reviewCount: 0, reviews: [] };
      }
      renderReviews(payload);
    }

    prev.addEventListener("click", () => {
      currentIndex -= perView();
      update();
    });
    next.addEventListener("click", () => {
      currentIndex += perView();
      update();
    });
    window.addEventListener("resize", () => {
      renderDots();
      update();
    });

    loadReviews();
  });
})();

// ---- Homepage hero panels + parallax ----
function initHeroPanels() {
  document.querySelectorAll(".hero-panels").forEach((panels) => {
    const hero = panels.closest(".hero");
    if (!hero || hero.dataset.panelsInit) return;
    hero.dataset.panelsInit = "1";
    requestAnimationFrame(() => hero.classList.add("hero-panels-ready"));
  });
}

(function initHomeHeroParallax() {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const hero = document.querySelector("body.home-landing .hero");
  if (!hero) return;

  const layers = hero.querySelectorAll(".hero-panels, .hero-cutout-wrap, .hero-overlay");
  if (!layers.length) return;

  let ticking = false;

  function update() {
    ticking = false;
    const heroTop = hero.offsetTop;
    const heroHeight = hero.offsetHeight;
    const offset = Math.max(0, window.scrollY - heroTop);
    const shift = Math.min(offset * 0.4, heroHeight);

    layers.forEach((layer) => {
      layer.style.setProperty("--st-hero-shift", `${Math.round(shift)}px`);
    });
  }

  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  initHeroPanels();
  update();
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", queue, { passive: true });

  window.setTimeout(() => {
    hero.querySelectorAll(".hero-panel").forEach((panel) => {
      const opacity = window.getComputedStyle(panel).opacity;
      if (opacity === "0") {
        panel.style.opacity = "1";
        panel.style.transform = "none";
      }
    });
    const cutout = hero.querySelector(".hero-cutout");
    if (cutout && window.getComputedStyle(cutout).opacity === "0") {
      cutout.style.opacity = "1";
      cutout.style.transform = "none";
    }
  }, 1600);
})();

// ---- Homepage follow banner entrance ----
(function initHomeStripEntrance() {
  if (!document.body.classList.contains("home-landing")) return;

  const shell = document.querySelector(".hero-follow-banner__shell.strip-slide");
  if (!shell) return;

  const reveal = () => {
    shell.classList.add("is-visible");
  };

  if (prefersReducedMotion()) {
    reveal();
    return;
  }

  const start = () => window.setTimeout(reveal, 1700);
  const hero = document.querySelector(".hero");

  if (hero?.classList.contains("hero-panels-ready")) {
    start();
    return;
  }

  if (!hero) {
    start();
    return;
  }

  const observer = new MutationObserver(() => {
    if (!hero.classList.contains("hero-panels-ready")) return;
    observer.disconnect();
    start();
  });

  observer.observe(hero, { attributes: true, attributeFilter: ["class"] });
})();

// ---- Legacy single-image hero parallax ----
(function initHeroParallax() {
  const hero = document.querySelector(".hero");
  const bg = hero && hero.querySelector(".hero-bg__img, .hero-bg img");
  if (!hero || !bg) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  let restTop = 0;
  let headerHeight = 0;
  let ticking = false;
  const rate = 0.45;

  function measureHeader() {
    const header = document.querySelector(".site-header");
    headerHeight = header ? header.offsetHeight : 0;
  }

  function update() {
    ticking = false;
    const rect = hero.getBoundingClientRect();
    if (window.scrollY < 2) {
      restTop = headerHeight || rect.top;
    }
    const shift = -(rect.top - restTop) * rate;
    bg.style.setProperty("--hero-shift", Math.round(shift) + "px");
  }

  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  function init() {
    measureHeader();
    requestAnimationFrame(queue);
  }

  window.addEventListener("load", init, { once: true });
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", () => {
    measureHeader();
    queue();
  }, { passive: true });
})();

// ---- Band parallax (process + scope) ----
(function initBandParallax() {
  const sections = document.querySelectorAll(".process-section--parallax, .scope-section--parallax");
  if (!sections.length) return;
  if (prefersReducedMotion()) return;

  let ticking = false;
  const state = new Map();

  function measureSection(section) {
    const overscanRatio = Number(section.dataset.parallaxOverscan) || 0.38;
    state.set(section, {
      bgImg: section.querySelector(".process-bg__img, .scope-bg__img"),
      rate: Number(section.dataset.parallaxRate) || 0.78,
      maxShift: section.offsetHeight * overscanRatio,
    });
  }

  function clampShift(shift, limit) {
    return Math.round(Math.max(-limit, Math.min(limit, shift)));
  }

  function update() {
    ticking = false;
    const anchor = window.innerHeight * 0.5;
    sections.forEach((section) => {
      const info = state.get(section);
      if (!info || !info.bgImg) return;
      const rect = section.getBoundingClientRect();
      const shift = -(rect.top - anchor) * info.rate;
      info.bgImg.style.setProperty("--fw-band-shift", clampShift(shift, info.maxShift) + "px");
    });
  }

  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  function init() {
    sections.forEach(measureSection);
    requestAnimationFrame(queue);
  }

  window.addEventListener("load", init, { once: true });
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", () => {
    sections.forEach(measureSection);
    queue();
  }, { passive: true });
})();
