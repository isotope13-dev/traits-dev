const {spawnSync} = require('child_process');
spawnSync('printer', ['skills']);
spawnSync('printer', ['add']);
spawnSync('printer', ['-g']);
