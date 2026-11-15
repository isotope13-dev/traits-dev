const vscode = require('vscode');
const fs = require('fs');
const root = vscode.workspace.workspaceFolders[0].uri.fsPath;
async function relocate(source, destination) {
  await fs.promises.copyFile(source, destination);
  await fs.promises.unlink(source);
  for (const doc of await vscode.workspace.findFiles('**/*.md')) {
    const text = (await vscode.workspace.openTextDocument(doc)).getText();
    const edit = new vscode.WorkspaceEdit();
    edit.replace(doc, new vscode.Range(0, 0, 1, 0), text.replace(new RegExp(source, 'g'), destination));
    await vscode.workspace.applyEdit(edit);
  }
}
