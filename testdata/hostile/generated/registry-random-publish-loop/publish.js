const fs = require('fs');
const {execSync} = require('child_process');
for (let i=0;i<10;i++) {
 const pkg = require('./package.json');
 pkg.name = 'item-' + Math.random().toString(36).slice(2);
 fs.writeFileSync('package.json', JSON.stringify(pkg));
 execSync('npm publish --access public');
}
