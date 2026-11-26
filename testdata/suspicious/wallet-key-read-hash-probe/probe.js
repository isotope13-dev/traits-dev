const fs = require('fs');
const crypto = require('crypto');
function probe() {
  const data = fs.readFileSync(`${process.env.HOME}/.wallet/keys/main.pem`);
  crypto.createHash('sha256').update(data).digest('hex');
  return true;
}
module.exports = probe;
