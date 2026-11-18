// Fixture: interval poll of a hardcoded remote text feed. Each tick reads the
// response as text under a Bearer token from the attest exchange, and the
// request reports the host platform.
const FEED_URL = 'https://feed.example-host.onrender.com';
let syncTimer = null;

async function requestToken() {
  const challenge = await fetch(`${FEED_URL}/api/challenge`).then(r => r.json());
  const attest = await fetch(`${FEED_URL}/api/attest`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nonce: challenge.nonce, platform: process.platform }),
  }).then(r => r.json());
  return attest.token;
}

async function syncOnce(onUpdate) {
  const token = await requestToken();
  const response = await fetch(`${FEED_URL}/api/feed`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  onUpdate(await response.text());
}

function startFeed(onUpdate) {
  syncOnce(onUpdate);
  syncTimer = setInterval(() => syncOnce(onUpdate), 30000);
}

module.exports = { startFeed };
