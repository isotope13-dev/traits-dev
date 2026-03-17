# Baseline Trait Review — Status

## Completed

~100 baseline traits moved from objectives/ to micro-behaviors/ or removed as duplicates:

- curl -s, wget -q, wget -O - → micro-behaviors/communications/http/download/cli-flags.yaml
- FlushInstructionCache, NtFlushInstructionCache → micro-behaviors/mem/sync/instruction-cache.yaml
- os.release, process.cwd → micro-behaviors/os/sysinfo/platform/node-apis.yaml
- JSON.stringify, JSON.parse → micro-behaviors/data/serialize/json/javascript.yaml
- Go base64 encode/decode → micro-behaviors/data/encode/base64/go.yaml
- Go bytes.Buffer → micro-behaviors/data/buffer/go.yaml
- which ufw/iptables/firewall-cmd → micro-behaviors/os/firewall/detection.yaml
- CheckRemoteDebuggerPresent → micro-behaviors/process/debug/detect/windows.yaml
- GetTokenInformation → micro-behaviors/process/privilege/token.yaml
- SetFileAttributes → micro-behaviors/fs/file/attributes/windows.yaml
- chdir symbol → micro-behaviors/fs/directory/mkdir/
- platform.system, platform.machine → micro-behaviors/os/sysinfo/platform/python.yaml (AST exact)
- apt-get, yum, dnf → already in micro-behaviors/os/package-manager/install/
- SHGetSpecialFolderLocation, SHGetPathFromIDListA, SHGetFolderPathW → micro-behaviors/fs/shell-ops/commands/
- os.makedirs, open(write) → already in micro-behaviors/fs/
- fs.readFile, readFileSync → already in micro-behaviors/fs/file/read/javascript.yaml

## Remaining (~63 baseline traits)

Most remaining baseline traits are attack-context-specific fragments that correctly
stay in objectives/:
- Mining pool hostnames and stratum protocol strings (objectives/impact/cryptojacking/)
- CVE-specific byte patterns and exploit fragments
- PyPI/npm packaging metadata (wheel, sdist, package types)
- JavaScript prototype pollution guard patterns (__proto__, constructor, prototype)
- CredFree, VaultClose (credential manager cleanup — only meaningful with CredRead)
- Binary metrics thresholds (section sizes, function counts)

These are composite building blocks with no meaning outside their attack context.
