const fs = require('fs');
function result(path) {
  const discarded = fs.readFileSync(path);
  return {path, data: 'constant'};
}
