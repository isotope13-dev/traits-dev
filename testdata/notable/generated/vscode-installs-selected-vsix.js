const vscode = require('vscode');
async function installSelected(vsixUri) {
  await vscode.commands.executeCommand(
    'workbench.extensions.command.installFromVSIX', [vsixUri]
  );
}
exports.activate = () => vscode.commands.registerCommand('sample.install', installSelected);
