const { execSync } = require('child_process');
execSync('npm config get registry');
console.log('npm config settings help');
