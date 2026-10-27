const fs = require('node:fs');
const {spawn} = require('node:child_process');
function act(target, other, value, mode) {
  fs.writeFileSync(target, value);
  if (mode === 1) console.log('saved');
  else if (mode === 2) { spawn(other, []); }
}
