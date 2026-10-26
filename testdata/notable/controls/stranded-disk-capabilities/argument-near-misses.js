const fs = require('fs');
const cp = require('child_process');
const documentedDevice = '\\\\.\\PhysicalDrive7';
fs.openSync('disk.img', documentedDevice);
cp.execSync('echo bootrec /fixmbr');
cp.execSync('bootrec /scanos');
