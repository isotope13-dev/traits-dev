const zlib = require('node:zlib');
const stream = zlib.createDeflate();
const handle = stream._handle;
handle.write(0, input, 0, input.length, output, 0, output.length);
stream.params(9, 0, () => {});
