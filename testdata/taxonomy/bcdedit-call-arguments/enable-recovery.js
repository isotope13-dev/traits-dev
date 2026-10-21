const {execSync}=require('child_process');
execSync('bcdedit /set {default} recoveryenabled Yes');
execSync('bcdedit /set {default} bootstatuspolicy DisplayAllFailures');
