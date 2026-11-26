const vscode = require('vscode');
const { spawn } = require('child_process');

// Spawn the CLI's refresh command detached on activation. The CLI owns any
// service registration; this extension only starts it once per activation.
function refreshOnActivate() {
  const child = spawn('anyray-helper', ['__spawn-refresh'], { detached: true, stdio: 'ignore' });
  child.on('error', () => {});
  child.unref();
}

function activate(context) {
  refreshOnActivate();
  context.subscriptions.push(vscode.commands.registerCommand('helper.status', () => 'ok'));
}

exports.activate = activate;
exports.deactivate = function () {};
