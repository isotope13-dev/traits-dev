const child_process_1 = require('child_process');
const NodePlatformArchToAbi = {linux: {x64: 'gnu'}};
exports.createHash = createHash;
const configDocs = 'https://docs.example.org/config/plugins.html';
function launch(script, args) {
  return (0, child_process_1.fork)(script, args);
}
function targets() {
  return this.chromeApi.debugger.getTargets();
}
const npmConfig = '.npmrc';
