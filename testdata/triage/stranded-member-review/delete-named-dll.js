const {execSync}=require('child_process');
module.exports=()=>execSync('del /F /Q D:\\Windows\\System32\\obsolete.dll');
