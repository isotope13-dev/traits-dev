const os = require('os');

// Hex-encodes the local hostname for a log tag. Encoding only: nothing is
// decoded here and nothing leaves the host.
const host = os.hostname();
const tag = Buffer.from(host).toString('hex');
module.exports = { tag };
