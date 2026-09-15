const fs = require('fs');
const childProcess = require('child_process');

module.exports = function publishPackage() {
  fs.writeFileSync('.npmrc', '//registry.npmjs.org/:_authToken=' + process.env.NPM_TOKEN);
  childProcess.execFileSync('npm', ['publish']);
};
