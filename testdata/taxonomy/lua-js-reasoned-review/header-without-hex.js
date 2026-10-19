const vm = require('vm');
module.exports.storage = Buffer.alloc(0xffff);
function load(headers, i, j, byte) {
  console.log(JSON.stringify(headers));
  module.exports.storage[i+j] = byte;
  vm.runInThisContext(module.exports.storage.toString());
}
