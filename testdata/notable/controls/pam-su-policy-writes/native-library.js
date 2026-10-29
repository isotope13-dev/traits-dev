import fs from 'node:fs';
fs.writeFileSync('/tmp/codec.so', new Uint8Array(8));
fs.createWriteStream('codec.dll');
