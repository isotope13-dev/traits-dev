const { spawnSync } = require('child_process');
spawnSync('npx', ['skills', 'add', source]);
spawnSync('tool', ['--global']);
