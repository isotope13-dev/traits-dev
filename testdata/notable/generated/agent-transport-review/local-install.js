const vscode = require('vscode');
async function install(localFile) {
  await vscode.commands.executeCommand('workbench.extensions.installExtension', vscode.Uri.file(localFile));
}
