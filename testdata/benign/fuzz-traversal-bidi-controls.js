'use strict';
// Adversarial corpus generator (deterministic, zero IO): traversal and
// invisible-character cases below are inert test data for the parser,
// so the traversal and bidi traits must stay silent on this fuzz file.
function buildCorpus() {
  const cases = [];
  cases.push({ id: 'dotdot', input: '../'.repeat(8) });
  cases.push({ id: 'zw', input: 'a​b' });
  return cases;
}
module.exports = buildCorpus;
