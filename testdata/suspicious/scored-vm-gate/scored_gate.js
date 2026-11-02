const { execSync } = require('child_process');
const AGENTS = ['VBoxService', 'vmtoolsd', 'xenservice'];
let score = 0;
const MODEL = execSync('wmic computersystem get model').toString();
if (/vmware|virtualbox/i.test(MODEL)) score += 50;
const MAC = queryMac();
if (MAC === "08:00:27") score += 30;
execSync('reg query HKLM\\HARDWARE\\DESCRIPTION\\System /v SystemBiosVersion');
const CIM = 'Get-CimInstance Win32_ComputerSystem';
collect(CIM);
if (score >= 50) { require('electron').app.quit(); }
