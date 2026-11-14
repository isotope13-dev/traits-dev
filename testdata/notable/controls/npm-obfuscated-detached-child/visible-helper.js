const table = ['one', 'two'];
while (!![]) {
  try {
    const offset = parseInt('42');
    if (offset === 42) break;
    table['push'](table['shift']());
  } catch (_error) {
    table['push'](table['shift']());
  }
}

const { spawn: launch } = require('child_process');
launch(process.execPath, ['-e', 'console.log("helper")'], {
  detached: false,
  stdio: 'inherit',
  windowsHide: false
});
