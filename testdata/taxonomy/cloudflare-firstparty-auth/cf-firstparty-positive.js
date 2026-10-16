// Release automation: the provider credential goes only to that provider's
// own API. Must not convict as harvesting or exfiltration.
const token = process.env.CLOUDFLARE_API_TOKEN;
const res = await fetch('https://api.cloudflare.com/client/v4/accounts/123', {
  headers: {authorization: `Bearer ${token}`},
});
export const ok = res.ok;
