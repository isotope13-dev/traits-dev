// Benign status poller: fetches a bearer-authenticated JSON status document on a
// timer and renders it. No attest handshake, no nonce echo, no module invocation
// of the fetched body.
const API = process.env.STATUS_API || 'https://status.example.com';

async function loadStatus(token) {
  const res = await fetch(`${API}/v1/status`, {
    headers: { Authorization: `Bearer ${token}`, Accept: 'application/json' },
  });
  if (!res.ok) throw new Error(`status ${res.status}`);
  return res.json();
}

function render(status) {
  console.log(`status: ${status.state}`);
}

setInterval(async () => {
  try {
    render(await loadStatus(process.env.STATUS_TOKEN));
  } catch (err) {
    console.error(err.message);
  }
}, 60000);
