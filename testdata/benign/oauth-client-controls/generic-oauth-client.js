// Generic first-party OAuth client: clientSecret here is vendor-neutral
// OAuth vocabulary and must never be attributed to any chat provider.
async function refreshAccessToken({ tokenUrl, clientId, clientSecret, refreshToken }) {
  const body = new URLSearchParams({
    grant_type: 'refresh_token',
    client_id: clientId,
    client_secret: clientSecret,
    refresh_token: refreshToken,
  });
  const res = await fetch(tokenUrl, { method: 'POST', body });
  return res.json();
}

module.exports = { refreshAccessToken };
