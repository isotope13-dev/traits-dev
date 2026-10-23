const https = require('https');
const options = { hostname: 'example.invalid' };
// options.rejectUnauthorized = false;
const example = "options['rejectUnauthorized'] = !1";
const insecure = options.rejectUnauthorized === false;
options.rejectUnauthorized = true;
options['rejectUnauthorized'] = !0;
https.request(options).end();
