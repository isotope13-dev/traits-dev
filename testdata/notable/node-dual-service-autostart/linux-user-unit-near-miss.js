import { writeFileSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";

const BIN = path.join(homedir(), ".example", "bin", "agent");

function systemdUnit() {
  return `[Unit]
Description=Example sync daemon

[Service]
ExecStart=${BIN} sync --once
Restart=on-failure

[Install]
WantedBy=default.target
`;
}

export function installUnit() {
  const unit = path.join(homedir(), ".config", "systemd", "user", "example-sync.service");
  writeFileSync(unit, systemdUnit());
  execFileSync("systemctl", ["--user", "enable", "--now", "example-sync"]);
  return unit;
}
