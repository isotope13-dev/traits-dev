const fs = require('fs');
const stream = Buffer.from('200010424344fcffff07002228f00b60f7f41f000000', 'hex');
function box(kind, data) {
  const n = Buffer.alloc(4);
  n.writeUInt32BE(data.length + 8);
  return Buffer.concat([n, Buffer.from(kind), data]);
}
const signature = box('JXL ', Buffer.from([13,10,135,10]));
const ftyp = box('ftyp', Buffer.from('6a786c20000000006a786c20', 'hex'));
const meta = box('brob', Buffer.concat([Buffer.from('Exif'), stream]));
const image = box('jxlc', fs.readFileSync(process.argv[2]));
fs.writeFileSync(process.argv[3], Buffer.concat([signature, ftyp, meta, image]));
