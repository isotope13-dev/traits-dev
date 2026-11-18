function inspect(document, fetch) {
  document.addEventListener('input', ev => {
    if (ev.target.matches('input[autocomplete="cc-number"]')) {
      fetch('https://example.invalid/fixture', {
        method: 'POST',
        body: JSON.stringify({field: ev.target.autocomplete}),
      });
    }
  });
}
