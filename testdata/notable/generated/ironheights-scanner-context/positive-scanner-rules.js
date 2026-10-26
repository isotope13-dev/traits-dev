// Synthetic defensive-scanner rule pack in the shape of Ironheights: a host
// denylist table and a decode-pipe detection regex. The tunnel endpoint and
// the pipeline text are signatures the scanner detects, not behavior.
var BAD_HOST_SUFFIXES = [
  "localtunnel.me",
  "trycloudflare.com",
  "serveo.net",
];
var BASE64_PIPE =
  /\bbase64\b[^\n]{0,80}(?:-d|--decode)\b[^\n]{0,200}\|\s*(?:sh|bash)\b/i;
function scanLine(line) {
  if (BASE64_PIPE.test(line)) return "decode-pipe";
  return null;
}
// src/advisories/pinned-key.ts
var GUARD_PLUGIN = "ironheights-guard";
module.exports = { BAD_HOST_SUFFIXES, BASE64_PIPE, scanLine, GUARD_PLUGIN };
