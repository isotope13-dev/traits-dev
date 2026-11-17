const vscode = require('vscode');
vscode.workspace.onDidChangeTextDocument(event => console.log(event.document.uri));
const compileCommand = `g++ -w source.cpp -o output`;
