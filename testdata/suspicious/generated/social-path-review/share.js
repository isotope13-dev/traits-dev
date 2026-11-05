async function share() {
  const url = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '')}`;
  vscode.env.openExternal(vscode.Uri.parse(url));
}
