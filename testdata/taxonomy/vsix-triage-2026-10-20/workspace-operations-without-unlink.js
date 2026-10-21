const vscode = require('vscode'); const fs = require('fs');
function folders() { return vscode.workspace.workspaceFolders; }
function list() { return vscode.workspace.findFiles('**/*.txt'); }
function open() { return workspace.openTextDocument('chosen.txt'); }
function edit(e) { return workspace.applyEdit(e); }
function copy(a,b) { return fs.copyFile(a,b); }
function remove(a) { return fs.promises.readFile(a); }
