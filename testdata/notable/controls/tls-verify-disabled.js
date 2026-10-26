const tls = require('tls');
tls.connect({host: 'example.invalid', rejectUnauthorized: false});
