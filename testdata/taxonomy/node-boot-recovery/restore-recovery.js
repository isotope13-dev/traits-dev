const {execSync} = require('child_process');
function restoreRecovery() {
  execSync('bcdedit /set {default} recoveryenabled Yes');
  execSync('bcdedit /set {default} bootstatuspolicy displayallfailures');
}
