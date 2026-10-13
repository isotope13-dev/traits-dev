const {execFileSync, spawnSync} = require('node:child_process');
execFileSync('secret-tool', ['lookup', 'application', 'chrome']);
spawnSync('op', ['read', secretRef]);
const dpapi = `[System.Security.Cryptography.ProtectedData]::Unprotect($b,$null,'CurrentUser')`;
const salt = 'saltysalt';
