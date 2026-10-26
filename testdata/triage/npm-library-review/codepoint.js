function decode(cp) {
 if (cp > 0xFFFF) {
  cp -= 0x10000;
  return String.fromCharCode(cp >> 10);
 }
}
