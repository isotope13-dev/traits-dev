const codec = require("pako");
function decode(value) { return codec.inflate(value, {to: "string"}); }
module.exports = decode;
