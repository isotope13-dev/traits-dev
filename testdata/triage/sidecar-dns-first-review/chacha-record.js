const crypto = require('node:crypto');
module.exports = (key, iv, record) => {
  const d = crypto.createDecipheriv("chacha20-poly1305", key, iv);
  d.setAuthTag(record.slice(0, 16));
  return Buffer.concat([d.update(record.subarray(16)), d.final()]);
};
