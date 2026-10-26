function clearPolicy() {
  document.querySelectorAll('meta[http-equiv="Content-Security-Policy"]').forEach(node => node.remove());
}
clearPolicy();
new MutationObserver(clearPolicy).observe(document.documentElement, {childList: true, subtree: true});
