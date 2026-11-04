const endpoint = 'https://discord.com/api/webhooks/000000000000000000/example';
async function share(consentStatus, file) {
  if (consentStatus !== 'true') { return false; }
  const success = await uploadFile(file);
  return success;
}
async function uploadFile(file) {
  const form = new FormData();
  form.append('file', file, 'report.html');
  return fetch(endpoint, {method: 'POST', body: form});
}
