const fs = require('fs');
const descriptor = fs.openSync('image.bin', 'r');
const contents = fs.readFileSync(descriptor);
