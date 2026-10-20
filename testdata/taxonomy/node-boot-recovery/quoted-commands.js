const {execSync} = require('child_process');
const examples = [
  'bcdedit /set {default} recoveryenabled No',
  'bcdedit /set {default} bootstatuspolicy ignoreallfailures'
];
function listBootSettings() { execSync('bcdedit /enum'); }
