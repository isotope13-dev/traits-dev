const fs = require('node:fs');
function cleanup(dir) {
 const files = fs.readdirSync(dir);
 for (const file of files) fs.unlinkSync(file);
}
