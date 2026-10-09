const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const host = path.join(vscode.env.appRoot, '/out/vs/workbench/workbench.desktop.main.js');
const html = 'workbench.html';
if (fs.existsSync(host)) fs.copyFileSync(host, host + '.bak');
fs.writeFileSync(host, 'custom editor UI');
