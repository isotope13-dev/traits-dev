const { exec } = require('child_process');
const path = require('path');
const installer = path.resolve(__dirname, 'installer.js');
exec(`powershell -NoProfile -WindowStyle Hidden -Command "Start-Process -FilePath '${process.execPath}' -ArgumentList '${installer}' -Verb RunAs -WindowStyle Hidden"`);
