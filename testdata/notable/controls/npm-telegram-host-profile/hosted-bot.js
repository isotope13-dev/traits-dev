const https = require('https');
https.request({ hostname: 'api.telegram.org', path: '/botTOKEN/sendMessage', method: 'POST' });
