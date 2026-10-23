// These functions are fixtures; never invoke the deliberately excessive loops.
function literal() {
  var buf = 'x';
  observe();
  for (var i = 0; i < 32; i++) { observe(); buf += buf; observe(); }
}
function decoded() {
  var payload = unescape('%u4141');
  for (j = 0; j <= 40; j++) { payload = payload + payload; }
}
function suffix() {
  var text = 'x';
  for (var k = 0; k < 100; k++) { text += text + '!'; }
}
