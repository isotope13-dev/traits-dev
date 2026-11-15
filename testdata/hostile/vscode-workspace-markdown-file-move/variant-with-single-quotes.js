const vscode = require('vscode');
const fs = require('fs');
const base = vscode.workspace.workspaceFolders[0].uri.fsPath;
async function move(input, output) {
  await fs.promises.copyFile(input, output);
  await fs.promises.unlink(input);
  const docs = await vscode.workspace.findFiles("docs/**/*.md");
  for (const uri of docs) {
    const doc = await vscode.workspace.openTextDocument(uri);
    const edit = new vscode.WorkspaceEdit();
    edit.replace(uri, new vscode.Range(doc.positionAt(0), doc.positionAt(doc.getText().length)), doc.getText().replace(input, output));
    await vscode.workspace.applyEdit(edit);
  }
}
