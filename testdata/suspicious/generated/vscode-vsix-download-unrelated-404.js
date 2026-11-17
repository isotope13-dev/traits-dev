const fs = require('fs');
const vscode = require('vscode');
async function install() {
const path = '/tmp/example.vsix';
await fetch('https://httpbin.org/download/example.vsix');
const response = await fetch('https://httpbin.org/bytes/8');
const bytes = await response.arrayBuffer();
await fs.promises.writeFile(path, bytes);
await vscode.commands.executeCommand('workbench.extensions.installExtension', vscode.Uri.file(path));
}
