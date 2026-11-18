"use strict";
// Hostile control: minimized from a marketplace AI-assistant extension whose
// webview ran remotely sourced scripts with no CSP and answered a readFile
// message carrying a webview-supplied path.
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
                case 'sendMessage':
                    await this.handleChat(message.payload.content);
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
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chat</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.0/marked.min.js"></script>
</head>
<body>
    <div id="chat"></div>
    <script>
        const vscode = acquireVsCodeApi();
        function addMessage(role, content) {
            const bubble = document.createElement('div');
            bubble.innerHTML = marked.parse(content);
            document.getElementById('chat').appendChild(bubble);
        }
        window.addEventListener('message', e => {
            if (e.data.type === 'fileContent') addMessage('assistant', e.data.payload.content);
        });
    </script>
</body>
</html>`;
    }
}
exports.ChatProvider = ChatProvider;
