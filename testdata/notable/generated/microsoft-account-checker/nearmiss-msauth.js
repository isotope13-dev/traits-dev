// Benign-looking OAuth helper: login host and generic status words, no inbox sweep.
const AUTH = "https://login.live.com/oauth20_authorize.srf?client_id=abc&response_type=code";
export function status(code) {
  if (code === 429) return "rotate";
  if (code === 401) return "twofa";
  return "ok";
}
export async function login(url) {
  return fetch(url, { headers: { Referer: "https://login.live.com/" } });
}
