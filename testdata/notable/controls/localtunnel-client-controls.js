// Benign control: CLI bundles the localtunnel client as an opt-in tunnel
// provider ("localtunnel", cloudflared, ngrok, remotosh, none). The endpoint
// is the client's documented default host; the status strings are the
// client's own error text, not provisioned C2 infrastructure.
const TUNNEL_DEFAULT_HOST = "https://localtunnel.me";
async function createLocaltunnel(port) {
  const localtunnel = await import("localtunnel");
  const tunnel = await localtunnel.default({ port, host: TUNNEL_DEFAULT_HOST });
  tunnel.on("error", (err) => {
    throw new Error(err && err.message || "localtunnel server returned an error, please try again");
  });
  tunnel.on("close", (code) => {
    throw new Error(`Localtunnel exited with code ${code}`);
  });
  setTimeout(() => {
    throw new Error("Localtunnel timeout");
  }, 30000).unref();
  return tunnel;
}
module.exports = { createLocaltunnel, tunnelProvider: "localtunnel" };
