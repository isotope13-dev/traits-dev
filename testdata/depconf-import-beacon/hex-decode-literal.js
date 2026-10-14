// Decodes a hex key delivered inside a string payload.
const payload = `key=${Buffer.from(k, "hex").toString()}`;
module.exports = { payload };
