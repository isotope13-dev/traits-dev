"""npm boolean feature flags are config, not credentials: only bare auth forms
and token-bearing names carry authentication material."""

const { spawnSync } = require("node:child_process");

const tailscaleAuth = process.env.npm_config_tailscale_auth === "true";
const bindMode = process.env.npm_config_bind || "loopback";

if (tailscaleAuth) {
  console.log(`dev mode: lan (${bindMode})`);
}

const status = spawnSync(
  "pnpm",
  ["--filter", "@dealdesk/db", "exec", "tsx", "src/migration-status.ts", "--json"],
  { encoding: "utf8" },
);
module.exports = { status: status.stdout.trim() };
