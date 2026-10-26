fetch('https://discord.com/api/webhooks/1234567890/abcdef-token', {
  method: 'POST',
  body: JSON.stringify({ content: 'hello' })
});
