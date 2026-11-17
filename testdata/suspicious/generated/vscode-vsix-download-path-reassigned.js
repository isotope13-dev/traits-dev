const fs = require('fs');
const vscode = require('vscode');
async function install() {
let path = '/tmp/download.vsix';
const response = await fetch('https://httpbin.org/download/example.vsix');
const bytes = await response.arrayBuffer();
await fs.promises.writeFile(path, bytes);
path = '/tmp/different.vsix';
await vscode.commands.executeCommand('workbench.extensions.installExtension', vscode.Uri.file(path));
}
