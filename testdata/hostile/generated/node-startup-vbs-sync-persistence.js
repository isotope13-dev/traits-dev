const fs = require('fs');
const path = require('path');
const os = require('os');
if (process.platform === 'win32') {
  const startup = path.join(os.homedir(), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup');
  const npmDir = path.join(process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming'), 'npm');
  const script = `Set WshShell = CreateObject("WScript.Shell")\nWshShell.Run """${path.join(npmDir, 'couplus-cli.cmd')}""", 0, False\n`;
  fs.writeFileSync(path.join(startup, 'couplus-cli.vbs'), script);
}
