const vscode = require('vscode');

function offerMemoryViewInstall() {
  vscode.window.showErrorMessage('Memory View is not installed.', 'Install MemoryView Extension')
    .then(choice => {
      if (choice === 'Install MemoryView Extension') {
        vscode.commands.executeCommand('workbench.extensions.installExtension', 'mcu-debug.memory-view');
      }
    });
}

module.exports = { offerMemoryViewInstall };
