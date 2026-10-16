// Release-integrity checker: verifies a downloaded artifact against its
// published hex digest before installing it.
const crypto = require('crypto');

const MD5_PATTERN = /^[a-fA-F0-9]{32}$/;
const SHA256_PATTERN = /^[a-fA-F0-9]{64}$/;

function looksLikeDigest(text, pattern) {
  return typeof text === 'string' && pattern.test(text.trim());
}

function verifyBuffer(data, expectedHex, algorithm) {
  if (!looksLikeDigest(expectedHex, algorithm === 'md5' ? MD5_PATTERN : SHA256_PATTERN)) {
    throw new Error('expected digest is not hex of the right length');
  }
  const actual = crypto.createHash(algorithm).update(data).digest('hex');
  return actual === expectedHex.trim().toLowerCase();
}

module.exports = { verifyBuffer, MD5_PATTERN, SHA256_PATTERN };
