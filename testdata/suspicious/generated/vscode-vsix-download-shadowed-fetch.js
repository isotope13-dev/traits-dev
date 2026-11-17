const fs = require('fs');
const vscode = require('vscode');
const fetch = async () => ({arrayBuffer: async () => new ArrayBuffer(0)});
async function install() {
const path = '/tmp/example.vsix';
const response = await fetch('https://httpbin.org/download/example.vsix');
const bytes = await response.arrayBuffer();
await fs.promises.writeFile(path, bytes);
await vscode.commands.executeCommand('workbench.extensions.installExtension', vscode.Uri.file(path));
}
