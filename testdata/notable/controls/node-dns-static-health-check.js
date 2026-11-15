const dns = require('dns');
const os = require('os');

const hostname = os.hostname();
dns.lookup('health.example.invalid', (error) => {
  if (error) console.error(hostname, error.message);
});
