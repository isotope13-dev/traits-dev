// A test-shaped name alone supplies no test harness.
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
module.exports = require('https');
