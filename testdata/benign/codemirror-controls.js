// Editor keyword table plus kill-ring accessors (cf. CodeMirror's MySQL
// mode and Emacs keymap): a language table listed as parenthesized strings
// is not concealed-string reconstruction, and a delegating tail call is a
// ring accessor, not an obfuscated string builder.
var keywords = wordRegexp([
  ('ACCESSIBLE'), ('ALTER'), ('AS'), ('BEFORE'), ('BINARY'), ('BY'),
  ('CASE'), ('SCHEMA'), ('SELECT'), ('SET'), ('SQL_BIG_RESULT'), ('SSL'),
  ('TABLE'), ('TINYBLOB'), ('TO'), ('TRUE'), ('UNIQUE'), ('UPDATE')
]);

var killRing = [];
function addToRing(str) {
  killRing.push(str);
  if (killRing.length > 50) killRing.shift();
}
function getFromRing() { return killRing[killRing.length - 1] || ""; }
function popFromRing() { if (killRing.length > 1) killRing.pop(); return getFromRing(); }
