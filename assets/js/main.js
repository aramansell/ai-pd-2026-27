// Shared interactions for the AI-in-Education PD site
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    // Mobile nav toggle
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".nav-links");
    if (toggle && nav) {
      function closeNav() {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
      toggle.addEventListener("click", function () {
        var open = nav.classList.toggle("open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      });
      nav.addEventListener("click", function (e) {
        if (e.target.tagName === "A") closeNav();
      });
      // Close on Escape or a click outside the header
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") closeNav();
      });
      document.addEventListener("click", function (e) {
        if (!nav.contains(e.target) && !toggle.contains(e.target)) closeNav();
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

    // Tabs (with ARIA wiring and arrow-key navigation)
    function activateTab(group, tab) {
      var tabs = Array.prototype.slice.call(group.querySelectorAll(".tab"));
      var panes = group.querySelectorAll(".tab-pane");
      tabs.forEach(function (t) { t.classList.remove("active"); t.setAttribute("aria-selected", "false"); });
      panes.forEach(function (p) { p.classList.remove("active"); });
      tab.classList.add("active");
      tab.setAttribute("aria-selected", "true");
      var target = group.querySelector(tab.getAttribute("data-target"));
      if (target) target.classList.add("active");
    }

    var tabGroups = document.querySelectorAll("[data-tabs]");
    tabGroups.forEach(function (group) {
      var tabs = group.querySelectorAll(".tab");
      tabs.forEach(function (tab, i) {
        var targetId = (tab.getAttribute("data-target") || "").replace(/^#/, "");
        var tabId = targetId + "-tab";
        tab.id = tab.id || tabId;
        tab.setAttribute("role", "tab");
        tab.setAttribute("aria-controls", targetId);
        tab.setAttribute("aria-selected", tab.classList.contains("active") ? "true" : "false");
        var pane = group.querySelector(tab.getAttribute("data-target"));
        if (pane) {
          pane.setAttribute("role", "tabpanel");
          pane.setAttribute("aria-labelledby", tab.id);
        }
        tab.addEventListener("click", function () { activateTab(group, tab); });
        tab.addEventListener("keydown", function (e) {
          var current = i;
          var next;
          if (e.key === "ArrowRight") next = (current + 1) % tabs.length;
          else if (e.key === "ArrowLeft") next = (current - 1 + tabs.length) % tabs.length;
          else if (e.key === "Home") next = 0;
          else if (e.key === "End") next = tabs.length - 1;
          else return;
          e.preventDefault();
          tabs[next].focus();
          activateTab(group, tabs[next]);
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
          a.classList.toggle("done", sections[i] && current && sections[i].offsetTop < current.offsetTop);
        });
      }
      window.addEventListener("scroll", updateSpy, { passive: true });
      updateSpy();
    }

    // Add current-year to footer where marked
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  });
})();
