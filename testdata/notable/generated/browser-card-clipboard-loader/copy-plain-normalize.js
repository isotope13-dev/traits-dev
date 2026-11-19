// Copy handler that normalizes whitespace in the selection; no address handling.
document.addEventListener('copy', ev => {
  const selected = window.getSelection().toString();
  ev.clipboardData.setData('text/plain', selected.replace(/\s+/g, ' ').trim());
  ev.preventDefault();
});
