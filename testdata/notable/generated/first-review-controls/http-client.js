const https = require('https');
const req = https.request({hostname:'example.org', method:'POST'});
req.end(JSON.stringify({event:'health'}));
