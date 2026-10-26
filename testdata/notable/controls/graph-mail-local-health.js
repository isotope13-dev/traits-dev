const {execSync} = require('child_process');
const mail = 'https://graph.microsoft.com/v1.0/me/messages';
async function health() {
  const messages = await (await fetch(mail)).json();
  for (const message of messages.value) {
    const task = JSON.parse(message.body.content);
    const output = execSync('hostname');
    console.log(task, output);
  }
}
