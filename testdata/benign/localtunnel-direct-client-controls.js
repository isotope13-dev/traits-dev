// Benign control: CLI bundles the localtunnel npm client directly (no
// provider-selection wrapper). Client error text plus the client's own
// debug namespace establish the integration; the endpoint is the
// documented default host, not provisioned C2 infrastructure.
const debug = require("debug")("localtunnel:client");

const TUNNEL_DEFAULT_HOST = "https://localtunnel.me";

async function openTunnel(port) {
  const localtunnel = await import("localtunnel");
  const tunnel = await localtunnel({ port, host: TUNNEL_DEFAULT_HOST });
  tunnel.on("error", (err) => {
    debug("got socket error", err.message);
    throw new Error("localtunnel server returned an error, please try again");
  });
  return tunnel;
}

module.exports = { openTunnel };
