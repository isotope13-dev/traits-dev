// An authenticated application record is returned as bytes, never executed.
const crypto = require('node:crypto');
module.exports = function decodeRecord(keyHex, ivHex, tagHex, dataHex, record) {
  const d = crypto.createDecipheriv("aes-128-gcm",
    Buffer.from(keyHex, "hex"), Buffer.from(ivHex, "hex"));
  d.setAuthTag(record.subarray(0, 16));
  return Buffer.concat([d.update(Buffer.from(dataHex, "hex")), d.final()]);
};
