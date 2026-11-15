const https = require('https');
const buildId = process.env.BUILD_ID;
const url = 'https://collect.telemetry.io/api?data=' + encodeURIComponent(buildId);
const parsed = new URL(url);
const req = https.request({ hostname: parsed.hostname, port: parsed.port || 443, path: parsed.pathname + parsed.search, method: 'GET' });
req.end();
