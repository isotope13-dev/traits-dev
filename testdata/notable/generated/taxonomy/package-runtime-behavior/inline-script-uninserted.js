function render(source) {
  const script = document.createElement('script');
  script.textContent = source;
  return script;
}
