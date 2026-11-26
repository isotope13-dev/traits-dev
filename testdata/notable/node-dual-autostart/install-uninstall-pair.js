// Opt-in `daemon install` / `daemon uninstall` pair for a CLI's own background worker.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const home = os.homedir();
const plistPath = path.join(home, 'Library', 'LaunchAgents', 'io.example.worker.plist');
const unitPath = path.join(home, '.config', 'systemd', 'user', 'example-worker.service');

export function install(nodeBin, cliJs) {
  if (process.platform === 'darwin') {
    const plist = `<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>Label</key><string>io.example.worker</string>
    <key>ProgramArguments</key>
    <array><string>${nodeBin}</string><string>${cliJs}</string><string>start</string></array>
    <key>RunAtLoad</key><true/>
</dict>
</plist>
`;
    fs.mkdirSync(path.dirname(plistPath), { recursive: true });
    fs.writeFileSync(plistPath, plist, 'utf-8');
    execFileSync('launchctl', ['load', '-w', plistPath]);
    return;
  }
  const unit = `[Unit]
Description=Example worker

[Service]
ExecStart=${nodeBin} ${cliJs} start
Restart=on-failure

[Install]
WantedBy=default.target
`;
  fs.mkdirSync(path.dirname(unitPath), { recursive: true });
  fs.writeFileSync(unitPath, unit, 'utf-8');
  execFileSync('systemctl', ['--user', 'enable', '--now', 'example-worker.service']);
}

export function uninstall() {
  if (process.platform === 'darwin') {
    try { execFileSync('launchctl', ['unload', plistPath]); } catch { /* not loaded */ }
    if (fs.existsSync(plistPath)) fs.unlinkSync(plistPath);
    return;
  }
  try { execFileSync('systemctl', ['--user', 'disable', '--now', 'example-worker.service']); } catch { /* not enabled */ }
  if (fs.existsSync(unitPath)) fs.unlinkSync(unitPath);
}
