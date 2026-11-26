const path = require('path');
const { execFileSync } = require('child_process');
const fixScript = path.resolve(__dirname, '../../../scripts/fix-better-sqlite3.cjs');
console.warn(`  rm -rf ${path.join(process.cwd(), 'node_modules')} ${path.join(process.cwd(), 'package.json')} ${path.join(process.cwd(), 'package-lock.json')}`);
