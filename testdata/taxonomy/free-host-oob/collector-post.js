export async function report(payload) {
  return fetch('https://webhook.site/12345678-1234-1234-1234-123456789abc', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}
