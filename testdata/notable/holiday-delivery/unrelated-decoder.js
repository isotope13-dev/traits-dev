async function notify(message) {
  await fetch('https://api.telegram.org/bot123456789:placeholder/sendMessage', {
    method: 'POST', body: JSON.stringify({ chat_id: '9876543210', text: message })
  });
}
notify('Build completed');

function decode(value) { return decodeUnsafe(value); }
