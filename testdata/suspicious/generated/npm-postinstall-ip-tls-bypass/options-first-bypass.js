import https from "https";

// Options-object-first https.get with verification disabled: the signature
// the TLS-bypass atom originally required. Must keep matching.
const req = https.get(
  { hostname: "updates.example.com", path: "/v1", rejectUnauthorized: false },
  (res) => {
    res.resume();
  },
);
req.on("error", () => {});
