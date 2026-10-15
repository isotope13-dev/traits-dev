// Positive control: heap-spray allocation paired with a spray-scale length
// recheck. After triggering the bug, the exploit re-reads a sprayed array's
// length to detect corruption.
var holders = [];
for (var i = 0; i < 200; i++) {
  var a = new Array(0x100000);
  holders.push(a);
}

function check(victim) {
  if (victim.length !== 0x100000) {
    return victim;
  }
  return null;
}

module.exports = { holders, check };
