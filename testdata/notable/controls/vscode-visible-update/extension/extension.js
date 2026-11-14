const https = require('https');
const fs = require('fs');
const path = require('path');
const vscode = require('vscode');
async function updateAfterConfirmation() {
  const approved = await vscode.window.showWarningMessage('Install update?', 'Install');
  if (approved !== 'Install') return;
  https.get('https://updates.example.invalid/release.zip', response => {
    response.pipe(fs.createWriteStream(path.join(__dirname, 'release.zip')));
  });
}
module.exports = { updateAfterConfirmation };
