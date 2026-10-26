function render(source, attrs) {
  const script = document.createElement("script");
  script.textContent = source;
  setScriptAttrs(script, attrs);
  document.head.appendChild(script);
}
