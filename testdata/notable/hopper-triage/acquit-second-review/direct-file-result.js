const fs = require('fs');
function result(path) {
  return {path, data: fs.readFileSync(path).toString('base64')};
}
