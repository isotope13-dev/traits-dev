const fs = require('fs');
const dirs = ['/', '/home'];
for (const dir of dirs) console.log(fs.readdirSync(dir));
