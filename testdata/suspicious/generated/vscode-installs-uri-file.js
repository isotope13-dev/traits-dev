const vscode = require('vscode');
function install(vsixPath) {
  return vscode.commands.executeCommand('workbench.extensions.installExtension', vscode.Uri.file(vsixPath));
}
