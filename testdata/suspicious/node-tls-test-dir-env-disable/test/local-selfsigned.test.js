// Local self-signed test server: the test opts out of TLS verification.
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
module.exports = { ok: true };
