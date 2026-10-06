// Codemod helper documenting the require shapes it rewrites:
//
//   `const x = require(imp)` and `const { x } = require(imp)`
//
// The mentions above live in a comment, and the generator below only
// builds require strings for the configs it writes; neither performs
// a dynamic require at runtime.
function requireFor(parser) {
  return `require('${parser}')`;
}

module.exports = { requireFor };
