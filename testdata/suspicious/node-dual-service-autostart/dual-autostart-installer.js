import { writeFileSync } from "node:fs";
import { homedir, platform } from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";

const LABEL = "dev.example.agent";
const BIN = path.join(homedir(), ".example", "bin", "agent");

function launchdPlist() {
  return `<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
  <key>Label</key><string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array><string>${BIN}</string><string>run</string></array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
</dict>
</plist>
`;
}

function systemdUnit() {
  return `[Unit]
Description=Example agent

[Service]
ExecStart=${BIN} run
Restart=always

[Install]
WantedBy=default.target
`;
}

export function installAutostart() {
  if (platform() === "darwin") {
    const plist = path.join(homedir(), "Library", "LaunchAgents", `${LABEL}.plist`);
    writeFileSync(plist, launchdPlist());
    return plist;
  }
  const unit = path.join(homedir(), ".config", "systemd", "user", "example-agent.service");
  writeFileSync(unit, systemdUnit());
  execFileSync("systemctl", ["--user", "enable", "--now", "example-agent"]);
  return unit;
}
