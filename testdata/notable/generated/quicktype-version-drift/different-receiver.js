const compression = require("pako");
const codec = require("balloon");
function decode(value) { return codec.inflate(value); }
module.exports = decode;
