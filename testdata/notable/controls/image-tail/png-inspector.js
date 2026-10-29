const fs = require('fs');
const image = fs.readFileSync(process.argv[2]);
const marker = Buffer.from([0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82]);
console.log(image.indexOf(marker));
