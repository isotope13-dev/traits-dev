// Ordinary module loading stays visible beside documentation or test syntax.
const example = "require('./.example.js')";
const runtime = require('../.runtime.js');
module.exports = { example, runtime };
