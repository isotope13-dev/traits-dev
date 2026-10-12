const {spawnSync} = require('child_process');
const installer = ['--yes', 'skills', 'add', '/local/package', '--skill', 'example', '-g', '-y'];
spawnSync('npx', [...installer], {stdio: 'inherit'});
