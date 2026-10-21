const {execSync}=require('child_process');
execSync("bcdedit /set {default} recoveryenabled No");
execSync("bcdedit /set {default} bootstatuspolicy ignoreallfailures");
