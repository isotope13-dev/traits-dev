const vscode = require('vscode');
const os = require('os');
const https = require('https');

function activate(context) {
  context.subscriptions.push(vscode.commands.registerCommand('profileConsent.send', async () => {
    const consent = await vscode.window.showWarningMessage('Send diagnostics?', 'Send');
    if (consent !== 'Send') return;
    const data = { username: os.userInfo().username, homeDir: os.homedir(), workingDir: process.cwd(), platform: process.platform };
    const request = https.request({ method: 'POST', hostname: 'telemetry.example.invalid', path: '/collect' });
    request.write(JSON.stringify(data));
    request.end();
  }));
}

module.exports = { activate };
