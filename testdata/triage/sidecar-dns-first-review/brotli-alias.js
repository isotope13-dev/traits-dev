const codec = require('node:zlib');
module.exports = bytes => codec.brotliDecompressSync(bytes);
