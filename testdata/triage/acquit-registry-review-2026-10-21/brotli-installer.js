// Static scanner fixture. Never execute.
const zlib = require('zlib');
const packed = 'setup.exe.br';
zlib.createBrotliDecompress();
const script = `Set sh = CreateObject("WScript.Shell")
sh.Run "setup.exe", 0, True`;
