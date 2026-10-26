const name = 'Gemini CLI'; const other = 'GitHub Copilot CLI';
const runtime = {sendMessage(message) {return message;}};
runtime.sendMessage({type: 'status_update'});
