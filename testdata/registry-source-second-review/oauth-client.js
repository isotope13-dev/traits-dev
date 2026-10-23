export async function exchange(code) {
  return fetch("https://auth.openai.com/oauth/token", {method: "POST", body: new URLSearchParams({grant_type: "authorization_code", code})});
}
