const zlib = require("zlib");
function transform(data) {
  zlib.brotliDecompressSync(data);
  zlib.gunzipSync(data);
  zlib.inflateSync(data);
  inflateSync(data);
  LZString.decompressFromUTF16(data);
  __import__.decompress(data);
  createBrotliDecompress();
  return new DecompressionStream("gzip");
}
