// Legacy query-string reader that keeps the decoder in a variable.
var decode = window.unescape;
function readParam(name) {
  var parts = location.search.substring(1).split("&");
  var out = {};
  for (var i = 0; i < parts.length; i++) {
    var kv = parts[i].split("=");
    out[kv[0]] = decode(kv[1] || "");
  }
  return out[name];
}
var title = decode("%u00e9t%u00e9");
document.title = readParam("q") || title;
