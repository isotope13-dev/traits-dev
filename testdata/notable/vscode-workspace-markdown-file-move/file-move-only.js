const fs = require('fs');
async function move(source, destination) {
  await fs.promises.copyFile(source, destination);
  await fs.promises.unlink(source);
}
