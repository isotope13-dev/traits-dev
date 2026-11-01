const crypto = require('crypto');
module.exports = { encrypt };
const digest = crypto.createHash('sha256');
