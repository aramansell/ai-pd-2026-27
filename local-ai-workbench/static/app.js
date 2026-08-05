/* AI Teacher Workbench - browser behaviour */
(function () {
  "use strict";

  // ---- Chat ----
  var form = document.getElementById("chat-form");
  var input = document.getElementById("chat-input");
  var log = document.getElementById("chat-log");

  function addBubble(role, text) {
    var el = document.createElement("div");
    el.className = "chat-" + role;
    var p = document.createElement("p");
    // Simple paragraph splitting + link safety.
    text.split(/\n{2,}/).forEach(function (block, i) {
      if (i > 0) p.appendChild(document.createElement("br"));
      var span = document.createElement("span");
      span.textContent = block;
      p.appendChild(span);
    });
    el.appendChild(p);
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
  }

  if (form && input && log) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = input.value.trim();
      if (!msg) return;
      addBubble("user", msg);
      input.value = "";
      input.focus();

      var typing = document.createElement("div");
      typing.className = "chat-bot chat-typing";
      typing.textContent = "Thinking...";
      log.appendChild(typing);
      log.scrollTop = log.scrollHeight;

      fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          typing.remove();
          if (data.error) {
            addBubble("bot", "Error: " + data.error);
          } else {
            addBubble("bot", data.reply);
          }
        })
        .catch(function () {
          typing.remove();
          addBubble("bot", "Could not reach the server. Is it still running?");
        });
    });
  }

  // ---- Prompt library ----
  var prompts = window.PROMPTS || [];
  var detail = document.getElementById("prompt-detail");
  var pdTitle = document.getElementById("pd-title");
  var pdHint = document.getElementById("pd-hint");
  var pdText = document.getElementById("pd-text");

  function selectPrompt(id) {
    var p = prompts.find(function (x) { return x.id === id; });
    if (!p) return;
    pdTitle.textContent = p.title;
    pdHint.textContent = p.hint || "";
    pdText.value = p.text;
    detail.hidden = false;
  }

  document.querySelectorAll(".prompt-card").forEach(function (card) {
    card.addEventListener("click", function () {
      selectPrompt(card.getAttribute("data-prompt-id"));
    });
  });

  document.getElementById("pd-copy").addEventListener("click", function () {
    pdText.select();
    try { document.execCommand("copy"); } catch (e) {}
    this.textContent = "Copied";
    var self = this;
    setTimeout(function () { self.textContent = "Copy"; }, 1500);
  });

  document.getElementById("pd-load").addEventListener("click", function () {
    if (input) { input.value = pdText.value; input.focus(); }
  });

  // ---- Status refresh ----
  var statusBox = document.getElementById("status-box");
  var refreshBtn = statusBox ? statusBox.querySelector(".status-refresh") : null;
  if (statusBox && refreshBtn) {
    refreshBtn.addEventListener("click", function () {
      this.textContent = "Checking...";
      fetch(statusBox.getAttribute("data-health-url"))
        .then(function (r) { return r.json(); })
        .then(function (h) {
          var text = statusBox.querySelector(".status-text");
          if (h.ok) {
            statusBox.className = "status-box status-ok";
            text.innerHTML = "Ready. Using " + h.provider + " with model \"" + h.model + "\".";
          } else {
            statusBox.className = "status-box status-bad";
            text.textContent = "Not ready: " + (h.message || "unknown issue") + " See SETUP.md.";
          }
          refreshBtn.textContent = "Refresh";
        })
        .catch(function () {
          refreshBtn.textContent = "Refresh";
        });
    });
  }
})();
