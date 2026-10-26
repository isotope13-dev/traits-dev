const codec = require("pako");
function run(value) { return eval(codec.inflate(value, {to: "string"})); }
module.exports = run;
