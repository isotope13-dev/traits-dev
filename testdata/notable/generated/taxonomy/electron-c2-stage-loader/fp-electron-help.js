// Benign Electron helper: opens the product help page in the browser.
// No decryption, no file drop, no telemetry POST.
const { app, BrowserWindow, shell } = require('electron');

function openHelp() {
  shell.openExternal('https://docs.example-app.net/help');
}

async function createWindow() {
  const win = new BrowserWindow({ width: 800, height: 600 });
  await win.loadFile('index.html');
  return win;
}

app.whenReady().then(createWindow);
module.exports = { openHelp };
