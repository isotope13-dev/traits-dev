async function request(url, authHeaders) {
  if (url.includes("https://webapi.bps.go.id/v1")) {
    const proxyBase = "https://api-proxy.example.invalid/v1";
    const rewrittenUrl = url.replace("https://webapi.bps.go.id/v1", proxyBase);
    return fetch(rewrittenUrl, { headers: { Accept: "application/json" } });
  }
  return fetch(url, { headers: { ...authHeaders } });
}
