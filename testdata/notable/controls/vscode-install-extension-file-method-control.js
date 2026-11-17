const vscode = require('vscode');
function installFromCatalog(catalog, extensionId) {
  return vscode.commands.executeCommand('workbench.extensions.installExtension', catalog.file(extensionId));
}
