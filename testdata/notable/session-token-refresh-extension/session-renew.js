// Session renewal: swap the current session token for a fresh one at our own auth service.
const API_BASE = 'https://api.fixture-vendor.test';

chrome.runtime.onInstalled.addListener(() => {});

async function renewSession(oky_token) {
  const r = await fetch(`${API_BASE}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token: oky_token }),
  });
  return r.ok ? r.json() : null;
}
