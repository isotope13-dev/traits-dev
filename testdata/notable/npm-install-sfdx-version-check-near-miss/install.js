const { execSync } = require('node:child_process');
const hasSfdx = (cmd) => {
  try {
    return execSync(`${cmd} --version`).toString('utf-8').includes('sfdx-cli/7.');
  } catch (e) {
    return false;
  }
};
if (hasSfdx('sfdx')) {
  throw new Error('sfdx is installed; remove sfdx-cli before installing sf');
}
