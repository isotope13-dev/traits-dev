const https = require('https');
const endpoint = 'https://webhook.site/12345678-1234-1234-1234-123456789abc';

https.get(endpoint + '?status=' + encodeURIComponent('ready')).on('error', () => {});
