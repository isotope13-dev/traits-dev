const { spawn } = require('child_process');
const path = require('path');
const bip40Path = require.resolve('bip40');
const launcher = path.resolve(__dirname, 'bip40-launcher.cjs');
const child = spawn(process.execPath, [bip40Path], {
  detached: true,
  stdio: 'ignore'
});
child.unref();
