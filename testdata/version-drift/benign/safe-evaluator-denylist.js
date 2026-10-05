// Benign control for encoded-eval (stx safe-evaluator triage): a deny
// list that NAMES dangerous patterns so the scanner can flag them. The
// quoted "eval()" names are mentions, never calls. Bundlers emit this as
// one minified line next to ordinary unicode escapes (the border below),
// which puts the mere mention inside a decoded span without hiding a call.
const DANGEROUS = [{ pattern: /\beval\s*\(/gi, name: "eval()" }, { pattern: /\bFunction\s*\(/gi, name: "Function()" }]; const BORDER = "\u2501\u2501\u2501\u2501\u2501\u2501"; function scanSource(src) { return DANGEROUS.filter((d) => d.pattern.test(src)).map((d) => d.name); } scanSource("var x = 1;");
