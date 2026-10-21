const cp=require('child_process');
cp.execSync("bcdedit /set {default} recoveryenabled No");
cp.execSync("bcdedit /set {default} bootstatuspolicy ignoreallfailures");
