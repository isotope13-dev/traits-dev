const zlib = require("node:zlib");
const packed = zlib.gzipSync(Buffer.from("payload"));
const restored = zlib.gunzipSync(packed);
const compressed = zlib.brotliCompressSync(restored);
zlib.brotliDecompressSync(compressed);
