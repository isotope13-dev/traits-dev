const {exec} = require('child_process');
function configureBoot() {
  exec('BCDEDIT.EXE /set {current} RECOVERYENABLED NO');
  exec('BCDEDIT.EXE /set {current} BOOTSTATUSPOLICY IGNOREALLFAILURES');
}
