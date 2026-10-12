// General-purpose free hosting can serve an ordinary application API.
export async function chat(messages) {
  const response = await fetch('https://assistant.gt.tc/api/chat.php', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages }),
  });
  return response.json();
}
