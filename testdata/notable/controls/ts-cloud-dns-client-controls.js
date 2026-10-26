// Benign control: ts-cloud-style DNS provider client. Reads the operator's
// own provider keys from the environment and POSTs them to the provider's
// own API to manage DNS records for a deployment.
const PORKBUN_API_KEY = process.env.PORKBUN_API_KEY
const PORKBUN_SECRET_KEY = process.env.PORKBUN_SECRET_KEY

async function addPorkbunARecord(domain, address) {
  const response = await fetch('https://api.porkbun.com/api/json/v3/dns/create/' + domain, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      apikey: PORKBUN_API_KEY,
      secretapikey: PORKBUN_SECRET_KEY,
      name: '@',
      type: 'A',
      content: address,
    }),
  })
  if (!response.ok) throw new Error('porkbun request failed')
  console.log('[ts-cloud] Created by ts-cloud DNS provider: ' + domain)
}

module.exports = { addPorkbunARecord }
