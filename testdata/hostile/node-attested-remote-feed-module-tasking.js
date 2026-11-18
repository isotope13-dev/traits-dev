// Minimal attested-feed loader: challenge nonce echoed to /api/attest, bearer
// token gates a feed GET, and the feed text is handed to a module call on a timer.
const feedModule = require('feed-runner');

const base = process.env.FEED_URL || 'https://feed.example.onrender.com';

async function fetchFeed() {
  const challenge = await (await fetch(`${base}/api/challenge`)).json();
  const attest = await (await fetch(`${base}/api/attest`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nonce: challenge.nonce, envKeys: [], platform: process.platform }),
  })).json();
  const token = attest.token;
  const response = await fetch(`${base}/api/feed`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.text();
}

setInterval(async () => {
  const text = await fetchFeed().catch(() => '');
  feedModule(text, true);
}, 30000);
