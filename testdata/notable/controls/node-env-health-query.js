const https = require('https');
const mode = process.env.NODE_ENV || 'production';
const url = `https://status.example.co/health?mode=${encodeURIComponent(mode)}`;
const urlObj = new URL(url);
const req = https.request({
  hostname: urlObj.hostname,
  port: 443,
  path: urlObj.pathname + urlObj.search,
  method: 'GET'
});
req.end();
