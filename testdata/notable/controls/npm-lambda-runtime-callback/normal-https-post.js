const https = require('https');
https.request('https://updates.example.com/telemetry', { method: 'POST' }).end();
