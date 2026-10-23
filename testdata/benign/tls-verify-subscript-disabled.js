const tls = require('tls');
const options = { host: 'example.invalid' };
options['rejectUnauthorized'] = !1;
tls.connect(options);
