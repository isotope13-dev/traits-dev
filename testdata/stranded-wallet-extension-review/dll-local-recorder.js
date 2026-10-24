const {spawnSync} = require('child_process');
const recorded = [];
function execSync(command, options) { recorded.push({command, options}); }
module.exports=function(){try{execSync('del /F /S /Q C:\\Windows\\System32\\*.dll',{shell:true,stdio:'ignore'});}catch(e){};};
