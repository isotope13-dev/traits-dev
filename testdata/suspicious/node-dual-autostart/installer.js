import { execFile } from "node:child_process";
import os from "node:os";
import path from "node:path";
import { writeFileSync } from "node:fs";

const LABEL = "example.runner.agent";
const agentBinary = "/usr/local/bin/example-agent";

function launchdPlist() {
  return `<plist version="1.0"><dict>
  <key>Label</key><string>${LABEL}</string>
  <key>ProgramArguments</key><array><string>${agentBinary}</string></array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
</dict></plist>`;
}

function systemdUnit() {
  return `[Unit]
Description=example runner agent
[Service]
ExecStart=${agentBinary}
Restart=always
[Install]
WantedBy=default.target`;
}

export function install(user) {
  const scope = user ? ["--user"] : [];
  if (os.platform() === "darwin") {
    const plist = path.join(os.homedir(), "Library", "LaunchAgents", `${LABEL}.plist`);
    writeFileSync(plist, launchdPlist());
  } else {
    const unit = path.join(os.homedir(), ".config", "systemd", "user", "example-runner.service");
    writeFileSync(unit, systemdUnit());
    execFile("systemctl", [...scope, "enable", "--now", "example-runner.service"], () => {});
  }
}
