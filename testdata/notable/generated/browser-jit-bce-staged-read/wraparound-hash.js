// Integer hash with 32-bit wraparound: the bitwise shape without any
// staged victim buffer, so the pattern without the heap grooming.
function hash32(h) {
  h = (h + 0x80000000) | 0;
  h = (h ^ (h >>> 16)) | 0;
  return h;
}

var table = new Uint8Array(256);
var digest = hash32(12345);
table[digest & 255] = 1;
