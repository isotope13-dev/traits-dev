// First-party app refreshing its own signed-in user's token.
async function refreshOwnToken() {
  const response = await fetch(
    `https://login.microsoftonline.com/${process.env.TENANT}/oauth2/v2.0/token`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        client_id: process.env.APP_CLIENT_ID,
        refresh_token: process.env.OWN_REFRESH_TOKEN,
        scope: 'https://graph.microsoft.com/Mail.Read offline_access',
      }),
    },
  );
  return response.json();
}

module.exports = { refreshOwnToken };
