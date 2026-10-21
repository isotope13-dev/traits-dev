// Static scanner fixture. Never execute.
const os = require('os');
const small = os.cpus().length < 2 || os.totalmem() < 2 * 1024 * 1024 * 1024;
if (small) throw new Error('sandbox analysis detected');
