const fs = require('fs');
const readFiles = ['.npmrc', '.env'];
const present = readFiles.map(file => ({ file, present: fs.existsSync(file) }));
console.log(JSON.stringify(present));
