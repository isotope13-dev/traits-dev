const vscode = require('vscode');
async function generate() {
  const code = vscode.window.activeTextEditor.document.getText();
  const response = await fetch('https://model.example.invalid/gpt', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({code})
  });
  return response.json();
}
