const { exec } = require('child_process');
const https = require('https');
const querystring = require('querystring');
const chatId = '123456789';
const botToken = '123456789:AAABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi';

function execShell(cmd) {
  return new Promise((resolve, reject) => exec(cmd, (err, stdout) =>
    err ? reject(err) : resolve(stdout.trim())));
}

function sendTelegramMessage(text) {
  const postData = querystring.stringify({ chat_id: chatId, text });
  return https.request({ hostname: 'api.telegram.org', path: `/bot${botToken}/sendMessage`, method: 'POST' });
}

async function report() {
  const [hostname, user] = await Promise.all([
    execShell('hostname'),
    execShell('whoami'),
  ]);
  await sendTelegramMessage(`Host: ${hostname}; User: ${user}`);
}

report();
