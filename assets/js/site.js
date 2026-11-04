(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Sticky header shadow + mobile action bar after the hero
  const hdr = $("[data-hdr]");
  const bar = $(".actionbar");
  const onScroll = () => {
    const y = scrollY;
    hdr && hdr.classList.toggle("is-stuck", y > 8);
    bar && bar.classList.toggle("is-on", y > 420);
  };
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Services dropdown (click + hover on desktop)
  $$(".nav__drop").forEach((drop) => {
    const btn = $(".nav__btn", drop);
    const set = (open) => { drop.classList.toggle("is-open", open); btn.setAttribute("aria-expanded", open); };
    btn.addEventListener("click", () => set(!drop.classList.contains("is-open")));
    drop.addEventListener("mouseenter", () => set(true));
    drop.addEventListener("mouseleave", () => set(false));
    drop.addEventListener("focusout", (e) => { if (!drop.contains(e.relatedTarget)) set(false); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") { set(false); } });
  });

  // Mobile drawer
  const drawer = $("[data-drawer]");
  const burger = $("[data-burger]");
  const openDrawer = (open) => {
    drawer.hidden = !open;
    burger.setAttribute("aria-expanded", open);
    document.body.classList.toggle("no-scroll", open);
    (open ? $("[data-close]", drawer) : burger).focus();
  };
  burger && burger.addEventListener("click", () => openDrawer(true));
  drawer && drawer.addEventListener("click", (e) => {
    if (e.target === drawer || e.target.closest("[data-close]")) openDrawer(false);
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && drawer && !drawer.hidden) openDrawer(false); });

  // Industry tabs (WAI-ARIA tabs pattern)
  $$("[data-tabs]").forEach((root) => {
    const tabs = $$('[role="tab"]', root);
    const select = (tab, focus) => {
      tabs.forEach((t) => {
        const on = t === tab;
        t.setAttribute("aria-selected", on);
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
      if (focus) tab.focus();
      tab.scrollIntoView({ block: "nearest", inline: "nearest", behavior: reduced ? "auto" : "smooth" });
    };
    tabs.forEach((t, i) => {
      t.addEventListener("click", () => select(t));
      t.addEventListener("keydown", (e) => {
        const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
        if (step) { e.preventDefault(); select(tabs[(i + step + tabs.length) % tabs.length], true); }
        if (e.key === "Home") { e.preventDefault(); select(tabs[0], true); }
        if (e.key === "End") { e.preventDefault(); select(tabs[tabs.length - 1], true); }
      });
    });
  });

  // Quote form: preselect service from ?service=, emergency nudge, inline validation
  $$("[data-form]").forEach((form) => {
    const need = $(".form__need", form);
    const alertBox = $("[data-emergency]", form);
    const pagePreset = $("[data-preset]");
    const preset = new URLSearchParams(location.search).get("service") || (pagePreset && pagePreset.dataset.preset);
    const radio = preset && $(`input[name="service"][value="${CSS.escape(preset)}"]`, form);
    if (radio) radio.checked = true;

    const syncNeed = () => {
      const val = (new FormData(form)).get("service");
      alertBox.hidden = val !== "emergency";
      if (val) need.classList.remove("is-invalid");
    };
    form.addEventListener("change", (e) => { if (e.target.name === "service") syncNeed(); });
    syncNeed();

    const check = (input) => {
      const field = input.closest(".field");
      if (!field) return true;
      const ok = input.checkValidity();
      field.classList.toggle("is-invalid", !ok);
      input.setAttribute("aria-invalid", !ok);
      return ok;
    };
    $$("input:not([type=radio]):not([type=file]), select, textarea", form).forEach((el) => {
      el.addEventListener("blur", () => { if (el.value) check(el); });
      el.addEventListener("input", () => { if (el.closest(".is-invalid")) check(el); });
    });

    const upload = $(".upload input", form);
    upload && upload.addEventListener("change", () => {
      const f = upload.files[0];
      if (f) $(".upload strong", form).textContent = f.name;
    });

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      let firstBad = null;
      if (!(new FormData(form)).get("service")) { need.classList.add("is-invalid"); firstBad = $('input[name="service"]', form); }
      $$("input[required]:not([type=radio]), input[type=email]", form).forEach((el) => {
        if (!check(el) && !firstBad) firstBad = el;
      });
      if (firstBad) { firstBad.focus(); return; }
      // Preview only: in WordPress this is a Contact Form 7 / Elementor form that emails the right department.
      const done = $("[data-done]", form);
      done.hidden = false;
      done.focus();
    });
  });

  // Reveal on scroll
  if (!reduced && "IntersectionObserver" in window) {
    const els = $$(".sec__head, .ind, .svc__card, .type, .step, .split__media, .split__body, .faq, .pcard, .feature, .case__aside, .card, .irow, .numlist li, .note");
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
    }), { rootMargin: "0px 0px -8% 0px" });
    els.forEach((el, i) => {
      el.classList.add("reveal");
      el.style.transitionDelay = `${(i % 4) * 60}ms`;
      io.observe(el);
    });
  }

  // Case study counter
  const num = $("[data-count]");
  if (num && !reduced && "IntersectionObserver" in window) {
    const target = +num.dataset.count;
    const io = new IntersectionObserver(([en]) => {
      if (!en.isIntersecting) return;
      io.disconnect();
      const t0 = performance.now();
      const tick = (t) => {
        const p = Math.min(1, (t - t0) / 1200);
        num.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }, { threshold: 0.5 });
    io.observe(num);
  }

  // Blog topic filters
  const filters = $$(".fchip");
  const grid = $("[data-posts]");
  filters.forEach((btn) => btn.addEventListener("click", () => {
    const f = btn.dataset.filter;
    filters.forEach((b) => b.setAttribute("aria-pressed", b === btn));
    let shown = 0;
    $$(".pcard", grid).forEach((c) => {
      const on = f === "all" || c.dataset.topic === f;
      c.hidden = !on;
      if (on) { shown++; c.classList.add("is-in"); }
    });
    $("[data-empty]").hidden = shown > 0;
  }));

  // Article reading progress + active TOC link
  const progressBar = $("[data-progress]");
  const prose = $("[data-prose]");
  if (progressBar && prose) {
    const tocLinks = $$(".toc a");
    const heads = tocLinks.map((a) => document.getElementById(a.hash.slice(1))).filter(Boolean);
    const update = () => {
      const r = prose.getBoundingClientRect();
      const p = Math.min(1, Math.max(0, -r.top / (r.height - innerHeight * 0.6)));
      progressBar.style.transform = `scaleX(${p})`;
      let cur = heads.filter((h) => h.getBoundingClientRect().top < 140).pop();
      tocLinks.forEach((a) => a.classList.toggle("is-active", cur && a.hash === "#" + cur.id));
    };
    addEventListener("scroll", update, { passive: true });
    update();
  }

  const yr = $("[data-year]");
  if (yr) yr.textContent = new Date().getFullYear();
})();
