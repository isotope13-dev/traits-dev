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
