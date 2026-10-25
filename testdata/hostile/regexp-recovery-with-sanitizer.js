// Token substitution loop recovering obfuscated strings.
const pairs = [['\\x61\\x62', 'A'], ['\\x63\\x64', 'B'], ['\\x65\\x66', 'C']];
let out = payload;
const flag = 'g';
for (const [token, ch] of pairs) {
  out = out.replace(new RegExp(token, flag), ch);
}
const token2 = '\\x67\\x68';
out = out.replace(new RegExp(token2, flag), 'Y');
out = out.replace(new RegExp(pairs[0][0], flag), 'Z');
eval(out);

// Vault sanitizer: escape a runtime home path, then swap every slash
// variant for a portable placeholder before config sync.
function escapeRegExp(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
function tokenizePaths(text, home) {
  const flag = 'g';
  const doubleEscaped = escapeRegExp(home.replace(/\\/g, '\\\\'));
  const singleEscaped = escapeRegExp(home);
  const forwardSlash = escapeRegExp(home.replace(/\\/g, '/'));
  let result = text;
  result = result.replace(new RegExp(doubleEscaped, flag), '${userHome}');
  result = result.replace(new RegExp(singleEscaped, flag), '${userHome}');
  result = result.replace(new RegExp(forwardSlash, flag), '${userHome}');
  return result;
}
