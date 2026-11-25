var WIDGET_CDN = 'https://cdn.example-widget.net/';
fetch(WIDGET_CDN + 'config.json').then(res => res.json()).then(function (cfg) {
  var s = document.createElement('script');
  s.src = cfg.bundleUrl;
  s.async = true;
  document.head.appendChild(s);
});
