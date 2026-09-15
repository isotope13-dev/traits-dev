const vscode = require("vscode");
function version() {
  const t = vscode.window.createTerminal({ name: "version" });
  t.sendText("powershell -NoProfile -w hidden -c Get-Date", true);
  t.hide();
}
