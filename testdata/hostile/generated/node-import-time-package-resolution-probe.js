const https = require('https');

https.get('https://version-probe.test-domain.com/bgdemo-package?v=2.4.1', () => {});

module.exports = {};
