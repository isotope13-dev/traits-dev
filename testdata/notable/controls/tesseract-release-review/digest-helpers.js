const {createHash} = require('crypto');
const int32 = [-2147483648, 2147483647];
const md5 = s => createHash('md5').update(s).digest('hex');
const sha256 = s => createHash('sha256').update(s).digest('hex');
const encoded = s => Buffer.from(s).toString('base64');
module.exports = {int32, md5, sha256, encoded};
