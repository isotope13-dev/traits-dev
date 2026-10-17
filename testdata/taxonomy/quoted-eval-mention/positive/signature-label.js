// Drainer signature table: the label names the pattern, never runs it.
var DRAINER_SIGNATURES = [
  [/eval\s*\(\s*atob\s*\(/i, "eval(atob( obfuscated script"],
  [/Function\s*\(\s*atob/i, "Function(atob( obfuscated script"]
];
module.exports = { DRAINER_SIGNATURES: DRAINER_SIGNATURES };
