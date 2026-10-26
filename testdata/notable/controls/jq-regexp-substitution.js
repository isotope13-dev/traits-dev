// jq-style text operations, returned as data rather than evaluated.
export function substitute(text, pattern, replacement, flags, global) {
  if (global) {
    const effective = flags.includes("g") ? flags : flags + "g";
    return text.replace(new RegExp(pattern, effective), replacement);
  }
  return text.replace(new RegExp(pattern, flags), replacement);
}
// A separate evaluator does not consume either replacement result.
export function evaluateExpression(expression) { return eval(expression); }
