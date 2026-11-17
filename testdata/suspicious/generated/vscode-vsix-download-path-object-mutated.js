const fs = require('fs');
const vscode = require('vscode');
async function install() {
const path = new URL('file:///tmp/download.vsix');
const response = await fetch('https://httpbin.org/download/example.vsix');
const bytes = await response.arrayBuffer();
await fs.promises.writeFile(path, bytes);
path.pathname = '/tmp/different.vsix';
await vscode.commands.executeCommand('workbench.extensions.installExtension', vscode.Uri.file(path));
}
