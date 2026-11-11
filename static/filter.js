// Topic/type filters for the Publications and Media pages.
// Without JavaScript the full list still shows (filters stay hidden).
(function () {
  document.querySelectorAll(".filters[data-filter-for]").forEach(function (panel) {
    var list = document.getElementById(panel.dataset.filterFor);
    if (!list) return;
    var rows = Array.prototype.slice.call(list.querySelectorAll(".row"));
    var older = list.querySelector("details.older");
    var empty = list.querySelector(".empty");
    var count = panel.querySelector(".count");
    var params = new URLSearchParams(window.location.search);
    var state = { topic: params.get("topic") || "all", type: params.get("type") || "all" };

    function apply() {
      var shown = 0;
      rows.forEach(function (r) {
        var ok = (state.topic === "all" || (" " + r.dataset.topics + " ").indexOf(" " + state.topic + " ") > -1) &&
                 (state.type === "all" || r.dataset.type === state.type);
        r.hidden = !ok;
        if (ok) shown++;
      });
      list.querySelectorAll("section.year").forEach(function (s) {
        s.hidden = !s.querySelector(".row:not([hidden])");
      });
      var filtering = state.topic !== "all" || state.type !== "all";
      if (older) {
        if (filtering) older.open = true;
        older.hidden = !older.querySelector(".row:not([hidden])");
      }
      if (empty) empty.hidden = shown > 0;
      panel.querySelectorAll(".pill").forEach(function (b) {
        b.setAttribute("aria-pressed", String(state[b.dataset.filter] === b.dataset.value));
      });
      count.textContent = filtering ? "Showing " + shown + " of " + rows.length : rows.length + " items";
      var q = new URLSearchParams();
      if (state.topic !== "all") q.set("topic", state.topic);
      if (state.type !== "all") q.set("type", state.type);
      var qs = q.toString();
      history.replaceState(null, "", qs ? "?" + qs : window.location.pathname);
    }

    panel.addEventListener("click", function (e) {
      var b = e.target.closest(".pill");
      if (!b) return;
      state[b.dataset.filter] = b.dataset.value;
      apply();
    });
    panel.hidden = false;
    apply();
  });
})();
