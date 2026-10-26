import https from "https";

// Loopback health check against a local proxy with a self-signed cert: skips
// verification but targets no remote endpoint. Must NOT match the dropper atom.
const req = https.get(
  { hostname: "127.0.0.1", port: 8443, rejectUnauthorized: false },
  (res) => {
    res.resume();
  },
);
req.on("error", () => {});
