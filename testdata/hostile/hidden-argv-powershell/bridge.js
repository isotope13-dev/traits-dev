const {execSync}=require("child_process");
const cmd=process.argv.slice(2).join(" ");
execSync(`powershell.exe -WindowStyle Hidden -Command ${cmd}`, {stdio:"ignore"});
