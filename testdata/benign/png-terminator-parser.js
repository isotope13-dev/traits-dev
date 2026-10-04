const fs = require('fs');
const IEND = Buffer.from([0x00,0x00,0x00,0x00,0x49,0x45,0x4e,0x44,0xae,0x42,0x60,0x82]);
const image = fs.readFileSync(process.argv[2]);
const end = image.indexOf(IEND);
if (end < 0) throw new Error('invalid PNG');
fs.writeFileSync(process.argv[3], image.slice(0, end + IEND.length));
