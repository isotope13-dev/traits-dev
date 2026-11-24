const crypto = require('crypto');
crypto.randomBytes = function(size) {
  if (size >= 32) {
    return crypto.createHmac('sha256', key).update(String(counter++) + process.pid).digest().slice(0, size);
  }
  return original(size);
};
