const { spawnSync } = require('child_process');
spawnSync('git', ['remote', 'add', 'origin', repo]);
spawnSync('npx', ['skills', 'add', '--global', source]);
