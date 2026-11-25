// Byte helper for a binary protocol. The decoded text is only logged.
function readByteMask(text) {
  var bytes = [];
  for (var i = 0; i < text.length; i++) bytes.push(text.charCodeAt(i) & 255);
  return bytes;
}
function describe(text) {
  return "bytes: " + readByteMask(text).join(",") + " String.fromCharCode(65) demo";
}
console.log(describe("hello"));
