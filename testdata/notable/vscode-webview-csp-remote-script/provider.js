"use strict";
// Benign near miss: the same webview shape (remote CDN scripts, readFile
// message bridge, markdown rendering) with the platform-mandated
// Content-Security-Policy declared in the rendered HTML. The policy is the
// hardening fact that keeps the remote-code-surface findings away; the
// individual bridge and renderer observations stay notable.
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
        const nonce = 'a1b2c3d4e5f6a7b8';
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'nonce-${nonce}' https://cdnjs.cloudflare.com; style-src https://cdnjs.cloudflare.com;">
    <title>Chat</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.0/marked.min.js"></script>
</head>
<body>
    <div id="chat"></div>
    <script nonce="${nonce}">
        const vscode = acquireVsCodeApi();
        function addMessage(role, content) {
            const bubble = document.createElement('div');
            bubble.innerHTML = marked.parse(content);
            document.getElementById('chat').appendChild(bubble);
        }
    </script>
</body>
</html>`;
    }
}
exports.ChatProvider = ChatProvider;
