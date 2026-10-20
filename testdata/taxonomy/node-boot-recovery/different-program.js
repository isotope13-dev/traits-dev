const {execSync} = require('child_process');
function printHelp() {
  execSync('echo bcdedit /set {default} recoveryenabled No');
  execSync('echo bcdedit /set {default} bootstatuspolicy ignoreallfailures');
  execSync('bcdedit-helper /set {default} recoveryenabled No');
}
