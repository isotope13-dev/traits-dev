const table = ['local', 'status', '1'];
function decode(index) { return table[index]; }
(function rotate(values) {
  while (!![]) {
    try {
      if (parseInt(values[0], 10) === 1) break;
      values['push'](values['shift']());
    } catch (_) {
      values['push'](values['shift']());
    }
  }
})(table);

const fs = require('fs');
function readStatus(file) {
  return fs.readFileSync(file, 'utf8');
}
module.exports = { readStatus };
