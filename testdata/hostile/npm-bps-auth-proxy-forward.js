async function request(url, authHeaders) {
  try {
    return await fetch(url, { headers: { ...authHeaders } });
  } catch (error) {
    if (url.includes("https://webapi.bps.go.id/v1")) {
      const proxyBase = "https://api-proxy.example.invalid/v1";
      const rewrittenUrl = url.replace("https://webapi.bps.go.id/v1", proxyBase);
      return fetch(rewrittenUrl, { headers: { Accept: "application/json", ...authHeaders } });
    }
    throw error;
  }
}
