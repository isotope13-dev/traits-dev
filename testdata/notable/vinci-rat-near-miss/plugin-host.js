// Electron main process for a desktop notes app: plugins run sandboxed in a
// VM context, and an "Open terminal here" menu item starts PowerShell.
const { app, BrowserWindow, Menu } = require('electron');
const vm = require('vm');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

function loadPlugin(file) {
  const code = fs.readFileSync(path.join(app.getPath('userData'), 'plugins', file), 'utf8');
  const sandbox = { console, exports: {} };
  vm.runInNewContext(code, sandbox, { filename: file, timeout: 1000 });
  return sandbox.exports;
}

function openTerminal(dir) {
  spawn('powershell.exe', ['-NoExit', '-Command', `Set-Location -LiteralPath '${dir}'`], { cwd: dir, detached: true });
}

async function checkForUpdates() {
  const res = await fetch('https://updates.example-notes.app/latest.json');
  return (await res.json()).version;
}

app.whenReady().then(() => {
  new BrowserWindow({ width: 900, height: 700 }).loadFile('index.html');
  Menu.setApplicationMenu(Menu.buildFromTemplate([{ label: 'Terminal', click: () => openTerminal(app.getPath('documents')) }]));
  for (const f of fs.readdirSync(path.join(app.getPath('userData'), 'plugins'))) loadPlugin(f);
  checkForUpdates();
});
