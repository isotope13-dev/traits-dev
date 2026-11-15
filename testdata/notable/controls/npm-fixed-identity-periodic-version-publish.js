const { execSync } = require('child_process');
const fs = require('fs');
const packageJson = require('./package.json');

function publishRelease() {
  packageJson.version = getNextVersion();
  fs.writeFileSync('package.json', JSON.stringify(packageJson));
  execSync('npm publish');
}

setInterval(publishRelease, 60000);
