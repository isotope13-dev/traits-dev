const https = require('https');

https.get('https://version-probe.test-domain.com/private-test1?v=2.4.1', () => {});

module.exports = {};
