const fs = require('fs');
const path = require('path');
function install(source) {
  const folder = path.join(process.env.APPDATA, 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup');
  const destination = path.join(folder, 'support.cmd');
  fs.mkdirSync(folder, {recursive: true});
  fs.copyFileSync(source, destination);
}
module.exports = {install};
