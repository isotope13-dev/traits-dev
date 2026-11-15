const fs = require('fs');
const path = require('path');

const manifest = fs.readFileSync(path.join(__dirname, 'package.json'), 'utf8');
const entries = fs.readdirSync(__dirname);
console.log('Package files:', entries.length, 'manifest bytes:', manifest.length);
