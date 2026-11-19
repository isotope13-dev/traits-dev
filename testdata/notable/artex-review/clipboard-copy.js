function copy(text) {
  const r = document.createElement('textarea');
  r.value = text;
  document.body.appendChild(r);
  document.execCommand('copy');
  document.body.removeChild(r);
}
