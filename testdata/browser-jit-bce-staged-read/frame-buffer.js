// Frame buffer for a software renderer: megabyte-scale but no
// wraparound-index probing, so staging without the exploit pattern.
var FRAME_BYTES = 8294400;
var frame = new Uint8Array(FRAME_BYTES);
frame.fill(0);

function putPixel(x, y, r, g, b) {
  var off = (y * 1920 + x) * 4;
  frame[off] = r;
  frame[off + 1] = g;
  frame[off + 2] = b;
}
putPixel(0, 0, 255, 0, 0);
