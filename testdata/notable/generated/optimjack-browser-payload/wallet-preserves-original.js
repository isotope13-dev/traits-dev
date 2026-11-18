document.addEventListener('copy', function(ev) {
  const selected = window.getSelection().toString();
  if (/^0x[a-fA-F0-9]{40}$/.test(selected)) {
    ev.clipboardData.setData('text/plain', selected);
  }
});
