function normalizeAppState(input) {
  return input.filter(cookie => cookie.key && cookie.value);
}

function looksLikeSession(cookies) {
  return cookies.some(cookie => cookie.key === "c_user" || cookie.key === "xs");
}

async function createSession(input) {
  const body = JSON.stringify({ jsonrpc: "2.0", appState: normalizeAppState(input) });
  return request("POST", "/v1/sessions", body, "https://fca-meta.neokex.xyz");
}
