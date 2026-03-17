# Baseline Trait Review

Atomic traits should be organized based on what they detect, not on what composite they serve.
Neutral capabilities (single API calls, keywords, syscalls) belong in `micro-behaviors/`
regardless of which objective composite references them.

These objectives/ directories contain baseline traits that may be neutral capabilities
misplaced for convenience alongside their composites. Each should be reviewed:
move neutral API/keyword detections to micro-behaviors/, keep attack-context-specific
fragments (e.g., mining pool hostnames, CVE-specific patterns) in objectives/.

## High priority (5+ baseline traits)

- [ ] `objectives/impact/cryptojacking/miner/` — 40 baseline traits (pool hostnames, stratum strings)
- [ ] `objectives/lateral-movement/supply-chain/npm/vulnerability/` — 10 baseline traits (JS path operations, proto guards)
- [ ] `objectives/discovery/system/fingerprint/` — 7 baseline traits (os.arch, os.release, process.cwd)
- [ ] `objectives/command-and-control/dropper/execution/loader/` — 6 baseline traits
- [ ] `objectives/impact/degrade/firewall/` — 5 baseline traits (iptables/ufw commands)

## Medium priority (2-4 baseline traits)

- [ ] `objectives/anti-static/obfuscation/tools/garble/` — 4 baseline traits (Go base64/buffer)
- [ ] `objectives/anti-static/obfuscation/control-flow/logic/` — 3 baseline traits
- [ ] `objectives/anti-static/obfuscation/binary-metrics/` — 2 baseline traits
- [ ] `objectives/command-and-control/backdoor/` — 3 baseline traits
- [ ] `objectives/command-and-control/beacon/network/` — 3 baseline traits (curl -s, wget -q)
- [ ] `objectives/evasion/file-hiding/dotfile-create/` — 3 baseline traits (os.makedirs, open write)
- [ ] `objectives/evasion/process/injection/` — 2 baseline traits (FlushInstructionCache)
- [ ] `objectives/evasion/process/hidden/filter/` — 2 baseline traits
- [ ] `objectives/execution/autoinstall/` — 3 baseline traits
- [ ] `objectives/lateral-movement/supply-chain/dropper/` — 3 baseline traits
- [ ] `objectives/lateral-movement/supply-chain/npm/code-quality/` — 2 baseline traits
- [ ] `objectives/lateral-movement/supply-chain/npm/malicious-patterns/` — 2 baseline traits (fs.readFile)
- [ ] `objectives/lateral-movement/supply-chain/pypi/install-patterns/` — 2 baseline traits (platform.system)
- [ ] `objectives/lateral-movement/supply-chain/pypi/metadata/` — 3 baseline traits (wheel/sdist)
- [ ] `objectives/persistence/login/startup/registry/` — 2 baseline traits
- [ ] `objectives/persistence/login/startup/startup-folder/` — 3 baseline traits
- [ ] `objectives/discovery/system/fingerprint/hardware/` — 2 baseline traits
- [ ] `objectives/discovery/system/fingerprint/machine-id/` — 2 baseline traits
- [ ] `objectives/credential-access/credential-manager/store-api/` — 2 baseline traits
- [ ] `objectives/anti-analysis/emulator-detect/` — 3 baseline traits
- [ ] `objectives/anti-analysis/sandbox-detect/` — 2 baseline traits
- [ ] `objectives/anti-static/obfuscation/payload/self-read/` — 2 baseline traits

## Low priority (1 baseline trait)

- [ ] `objectives/anti-analysis/debugger-detect/check/` — CheckRemoteDebuggerPresent
- [ ] `objectives/anti-analysis/environment-detect/wsh/` — typeof check
- [ ] `objectives/anti-analysis/self-modify/runtime/` — 1 trait
- [ ] `objectives/anti-analysis/timing/evasion/` — 1 trait
- [ ] `objectives/anti-analysis/timing/jitter/` — 1 trait
- [ ] `objectives/anti-static/obfuscation/code-metrics/` — 1 trait
- [ ] `objectives/anti-static/obfuscation/code-metrics/functions/` — 1 trait
- [ ] `objectives/anti-static/obfuscation/encoding/` — 1 trait
- [ ] `objectives/anti-static/obfuscation/payload/` — 1 trait
- [ ] `objectives/anti-static/obfuscation/payload/encrypted/` — 1 trait
- [ ] `objectives/anti-static/obfuscation/payload/section/` — 1 trait
- [ ] `objectives/anti-static/pack/detect/` — UPX marker
- [ ] `objectives/collection/clipboard/capture/` — 1 trait
- [ ] `objectives/collection/keylog/capture/` — 1 trait
- [ ] `objectives/command-and-control/beacon/network/periodic/` — 1 trait
- [ ] `objectives/command-and-control/channel/p2p/` — 1 trait
- [ ] `objectives/command-and-control/channel/tunnel/proxy/` — 1 trait
- [ ] `objectives/command-and-control/dropper/behavior/` — 1 trait
- [ ] `objectives/command-and-control/infrastructure/ip/` — 1 trait
- [ ] `objectives/credential-access/clipboard/crypto/` — 1 trait
- [ ] `objectives/discovery/network/enumeration/` — 1 trait
- [ ] `objectives/discovery/network/scan/` — 1 trait
- [ ] `objectives/discovery/network/scan/port/` — 1 trait
- [ ] `objectives/discovery/system/fingerprint/os/` — 1 trait
- [ ] `objectives/evasion/anti-av/edr-detect/wmi/` — 1 trait
- [ ] `objectives/evasion/anti-av/ntdll-unhook/` — 1 trait
- [ ] `objectives/evasion/file-hiding/attributes/` — SetFileAttributes
- [ ] `objectives/evasion/masquerade/` — 1 trait
- [ ] `objectives/execution/exploit/actionscript/` — 1 trait
- [ ] `objectives/execution/lnk/dropper/` — 1 trait
- [ ] `objectives/exfiltration/http/` — 1 trait
- [ ] `objectives/impact/crypto-manipulation/clipboard/` — 1 trait
- [ ] `objectives/impact/cryptojacking/wallet/` — 1 trait
- [ ] `objectives/impact/degrade/edr/targeting/` — 1 trait
- [ ] `objectives/lateral-movement/exploit/redis/` — 1 trait
- [ ] `objectives/lateral-movement/supply-chain/npm/` — 1 trait
- [ ] `objectives/lateral-movement/supply-chain/npm/minifier/` — 1 trait
- [ ] `objectives/persistence/login/registry/run-key/` — 1 trait
- [ ] `objectives/persistence/system/daemon/init/` — chdir symbol
- [ ] `objectives/persistence/system/wmi/subscription/` — 1 trait
- [ ] `objectives/privilege-escalation/token-manipulation/` — 1 trait
