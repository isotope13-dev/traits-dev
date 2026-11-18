"use strict";
// Benign near miss: a script-enabled webview with a readFile message bridge
// that renders markdown through a sanitizing pipeline (DOMPurify wraps the
// marked output) and loads no remote scripts. The sanitizer between the
// parse and the innerHTML assignment, and the absence of remote script
// sources, keep both hostile bridge composites away.
const vscode = require("vscode");
class ChatProvider {
    constructor(extensionUri) {
        this.extensionUri = extensionUri;
    }
    resolveWebviewView(webviewView) {
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this.extensionUri]
        };
        webviewView.webview.html = this.getHtml(webviewView.webview);
        webviewView.webview.onDidReceiveMessage(async (message) => {
            switch (message.type) {
                case 'readFile':
                    const content = await this.readFile(message.payload.path);
                    webviewView.webview.postMessage({ type: 'fileContent', payload: content });
                    break;
            }
        });
    }
    async readFile(path) {
        const uri = vscode.Uri.file(path);
        const bytes = await vscode.workspace.fs.readFile(uri);
        return Buffer.from(bytes).toString('utf8');
    }
    getHtml(webview) {
        const markedUri = webview.asWebviewUri(vscode.Uri.joinPath(this.extensionUri, 'media', 'marked.min.js'));
        const purifyUri = webview.asWebviewUri(vscode.Uri.joinPath(this.extensionUri, 'media', 'purify.min.js'));
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chat</title>
    <script src="${markedUri}"></script>
    <script src="${purifyUri}"></script>
</head>
<body>
    <div id="chat"></div>
    <script>
        const vscode = acquireVsCodeApi();
        function addMessage(role, content) {
            const bubble = document.createElement('div');
            bubble.innerHTML = DOMPurify.sanitize(marked.parse(content));
            document.getElementById('chat').appendChild(bubble);
        }
    </script>
</body>
</html>`;
    }
}
exports.ChatProvider = ChatProvider;
