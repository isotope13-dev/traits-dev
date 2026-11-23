async function createSession(input) {
  const body = JSON.stringify({ appState: input });
  return request("POST", "/v1/sessions", body, "https://fca-meta.neokex.xyz");
}
