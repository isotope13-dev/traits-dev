(function () {
  var onPhone = window.matchMedia("(max-width: 768px)").matches;
  if (window.location.pathname.includes("/checkout/success")) {
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=AW-123456789";
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: "purchase", device: onPhone ? "mobile" : "desktop" });
  }
})();
