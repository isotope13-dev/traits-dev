const fs = require('fs');
const fd = fs.openSync('PhysicalDrive7.img', 'r+');
fs.closeSync(fd);
const instructions = 'bootrec /fixmbr';
console.log(instructions);
