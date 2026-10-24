const endpoint = 'https://login.microsoftonline.com/organizations/oauth2/v2.0/token';
const client_id = 'application-id';
const response = await fetch(endpoint, {
  method: 'POST', body: new URLSearchParams({username: account, password: candidate,
    grant_type: 'password', client_id: client_id,
    scope: 'https://graph.microsoft.com/.default'})
});
console.log(response.status);
