const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');

function activate(context) {
  context.subscriptions.push(vscode.commands.registerCommand('visibleInstaller.run', async () => {
    const choice = await vscode.window.showWarningMessage('Run the visible tool installer?', 'Run');
    if (choice !== 'Run') return;
    const scriptPath = context.asAbsolutePath('scripts/install.bat');
    exec(`"${scriptPath}"`, { cwd: path.dirname(scriptPath) });
  }));
}

module.exports = { activate };
