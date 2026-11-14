const https = require('https');
https.get({ hostname: 'collector.m.pipedream.net', path: '/', method: 'GET' }, res => res.resume());
