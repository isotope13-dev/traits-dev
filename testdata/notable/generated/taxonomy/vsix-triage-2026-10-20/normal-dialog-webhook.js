const vscode = require('vscode');
const axios = require('axios');
async function run() {
 const input = await vscode.window.showInputBox({title:'Release message'});
 const target = 'https://discord.com/api/webhooks/123/test';
 await publish(target, `Message: ${input}`);
}
async function publish(url, message) { await axios.post(url, {content:message}); }
