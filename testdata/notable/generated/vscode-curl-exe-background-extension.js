const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');

async function activate(context) {
  const scriptPath = context.asAbsolutePath('scripts/run.bat');
  exec(`"${scriptPath}"`, { cwd: path.dirname(scriptPath), windowsHide: true });
}

module.exports = { activate };
