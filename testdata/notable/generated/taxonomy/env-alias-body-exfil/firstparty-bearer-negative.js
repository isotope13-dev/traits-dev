// First-party auth: the provider credential goes only to that provider's
// own API as a header. Must stay clean.
const token = process.env.CLOUDFLARE_API_TOKEN;
const res = await fetch('https://api.cloudflare.com/client/v4/accounts/123', {
  headers: {authorization: `Bearer ${token}`},
});
export const ok = res.ok;
