function comparison() {
  var buf = 'x';
  for (var i = 0; i < 100; i++) { buf == buf + buf; }
}
function shortLoop() {
  var buf = 'x';
  for (var i = 0; i < 31; i++) { buf += buf; }
}
function otherSource() {
  var buf = 'x';
  for (var i = 0; i < 100; i++) { buf += other; }
}
function otherDecoder() {
  var buf = decode('x');
  for (var i = 0; i < 100; i++) { buf += buf; }
}
function guardedExit() {
  var buf = 'x';
  for (var i = 0; i < 100; i++) { observe(); if (buf.length > 10) break; buf += buf; }
}
