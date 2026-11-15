const cookie = require('cookie');
const signature = require('cookie-signature');
exports.signedCookie = (value, secret) => signature.unsign(value, secret);
exports.parse = (header) => cookie.parse(header);
