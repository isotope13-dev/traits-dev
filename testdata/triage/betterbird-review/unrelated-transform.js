const zlib = require('zlib');
module.exports = b => zlib.brotliDecompressSync(b);
