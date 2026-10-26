// [System.Security.Cryptography.ProtectedData]::Unprotect(...)
const docs = 'secret-tool lookup and op read';
execFileSync('echo', ['secret-tool', 'lookup']);
spawnSync('op', ['--version']);
execFileSync('secret-tool', ['--help']);
