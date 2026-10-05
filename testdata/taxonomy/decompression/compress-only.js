const zlib = require("zlib");
function transform(data) { return zlib.gzipSync(data); }
