// Compatibility shim: loads a local polyfill on iPad.
if (/iPhone|iPad/.test(navigator.userAgent)) {
  const s = document.createElement('script');
  s.src = '/static/js/ipad-polyfill.js';
  document.head.appendChild(s);
}
