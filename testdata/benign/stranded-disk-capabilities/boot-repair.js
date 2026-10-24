const cp = require('child_process');
// Repair commands remain notable in legitimate administration code.
module.exports = function repairBootRecord() {
  cp.execSync('BOOTREC.EXE /FIXMBR', {stdio: 'inherit'});
};
