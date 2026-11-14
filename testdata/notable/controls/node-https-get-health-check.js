const https = require('https');
https.get({ hostname: 'updates.example.com', path: '/status', method: 'GET' }, res => res.resume());
