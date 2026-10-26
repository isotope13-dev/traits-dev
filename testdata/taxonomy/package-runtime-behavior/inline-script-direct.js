function render(source) {
  const element = document.createElement('script');
  element.textContent = source;
  document.body.appendChild(element);
}
