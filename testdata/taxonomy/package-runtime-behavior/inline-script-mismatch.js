function render(source, other) {
  const script = document.createElement('script');
  other.textContent = source;
  document.head.appendChild(script);
}
