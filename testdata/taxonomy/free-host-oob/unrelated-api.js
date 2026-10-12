export async function chat(messages) {
  const response = await fetch('https://api.example.com/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages }),
  });
  return response.json();
}
