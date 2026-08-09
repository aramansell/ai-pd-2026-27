// Shared interactions for the AI-in-Education PD site
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    // Mobile nav toggle
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".nav-links");
    if (toggle && nav) {
      toggle.addEventListener("click", function () {
        nav.classList.toggle("open");
        var label = toggle.getAttribute("aria-expanded") === "true" ? "false" : "true";
        toggle.setAttribute("aria-expanded", label);
      });
      nav.addEventListener("click", function (e) {
        if (e.target.tagName === "A") nav.classList.remove("open");
      });
    }

    // Accordion
    document.querySelectorAll(".acc-item").forEach(function (item) {
      var head = item.querySelector(".acc-head");
      if (!head) return;
      head.setAttribute("aria-expanded", "false");
      head.addEventListener("click", function () {
        var open = item.classList.toggle("open");
        head.setAttribute("aria-expanded", open ? "true" : "false");
      });
    });

    // Tabs
    var tabGroups = document.querySelectorAll("[data-tabs]");
    tabGroups.forEach(function (group) {
      var tabs = group.querySelectorAll(".tab");
      tabs.forEach(function (tab) {
        tab.addEventListener("click", function () {
          tabs.forEach(function (t) { t.classList.remove("active"); });
          group.querySelectorAll(".tab-pane").forEach(function (p) { p.classList.remove("active"); });
          tab.classList.add("active");
          var target = group.querySelector(tab.getAttribute("data-target"));
          if (target) target.classList.add("active");
        });
      });
    });

    // Session progress nav (scrollspy) — highlights the section you're in
    var sessionNav = document.querySelector(".session-nav");
    if (sessionNav) {
      var links = Array.prototype.slice.call(sessionNav.querySelectorAll("a[href^='#']"));
      var sections = links.map(function (a) {
        return document.querySelector(a.getAttribute("href"));
      }).filter(Boolean);

      function updateSpy() {
        var pos = window.scrollY + 140; // offset for sticky header + session nav
        var current = null;
        sections.forEach(function (sec) {
          if (sec.offsetTop <= pos) current = sec;
        });
        links.forEach(function (a, i) {
          var on = sections[i] === current;
          a.classList.toggle("active", on);
          // mark everything above the current section as "done"
          a.classList.toggle("done", sections[i] && current && sections[i].offsetTop < current.offsetTop);
        });
      }
      window.addEventListener("scroll", updateSpy, { passive: true });
      updateSpy();
    }

    // Auto-open print-friendly? (no)
    // Add current-year to footer where marked
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  });
})();
