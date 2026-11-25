// Stager: decodes a byte-masked payload and runs it through indirect eval.
var KEY = 0x5a;
function decodeStage(encoded) {
  var out = "";
  for (var i = 0; i < encoded.length; i++) {
    var b = encoded.charCodeAt(i) & 255;
    out += String.fromCharCode(b ^ KEY);
  }
  return out;
}
var stage = decodeStage("\u0014\u0015\u0013\u0014\u0014\u0013");
(0, eval)(stage);
