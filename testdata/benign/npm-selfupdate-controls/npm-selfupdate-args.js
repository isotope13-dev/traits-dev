'use strict';
// Control: a self-updater fragment that builds a global install invocation
// from parts and executes it through the package manager.
const { execFileSync } = require('child_process');

function upgradeArgs(manager, version) {
  const spec = `mycli@${version || 'latest'}`;
  if (manager === 'npm') return ['install', '-g', spec];
  return ['add', '-g', spec];
}

execFileSync('npm', upgradeArgs('npm', '1.2.3'));
