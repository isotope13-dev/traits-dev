function render(source) {
  let script = document.createElement('script');
  script = document.createElement('div');
  script.textContent = source;
  document.head.appendChild(script);
}
