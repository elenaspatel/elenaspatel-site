// Turn "user [at] domain [dot] edu" into a working mailto link. The full address never
// appears in the HTML, so simple scrapers that don't run JavaScript can't harvest it.
document.querySelectorAll("a.js-email").forEach(function (a) {
  var addr = a.dataset.u + "@" + a.dataset.d;
  a.href = "mailto:" + addr;
  a.textContent = addr;
});
