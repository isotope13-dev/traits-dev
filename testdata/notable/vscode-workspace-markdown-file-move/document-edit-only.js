const vscode = require('vscode');
async function normalize() {
  for (const doc of await vscode.workspace.findFiles('**/*.md')) {
    const open = await vscode.workspace.openTextDocument(doc);
    const edit = new vscode.WorkspaceEdit();
    edit.replace(doc, new vscode.Range(0, 0, 1, 0), open.getText().replace(/old/g, 'new'));
    await vscode.workspace.applyEdit(edit);
  }
}
