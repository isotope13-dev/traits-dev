const {execSync}=require('child_process');
module.exports=()=>{execSync('bcdedit /set {current} bootstatuspolicy displayallfailures');execSync('bcdedit /set {current} recoveryenabled yes');};
