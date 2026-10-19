Reviewed samples
================

1e20bc257f7c637a95f935d613d9a9c17eede935f3ed96c1edd8c96c1cf6403e
systemd-ntpd: BENIGN, XMRig 6.26.0 Linux static x64 miner plus an inert trailer.

cb97d361fe7ab33d459812b6c4ae6b8b73dfbf7d0e19ce924782df8bf7ce13d6
ddCopyNegate.decTest: BENIGN, IBM General Decimal Arithmetic test vectors.

c841368e096af9ebe6a10049634ee14ff9a1dd06199dff0ccc73e8fb8fb82cb5
powersqrt.decTest: BENIGN, IBM General Decimal Arithmetic test vectors.

Evidence and execution paths
============================

Ran atomscan in slow mode and cleave facts on every sample, including extracted
and decoded text. Neither decimal file has symbols, executable code, included
test files, network operations, or dependencies. Every non-comment line parses
as a context directive or an operation/operand/expected-result row. There are
43 copynegate cases and 2,856 power cases, respectively. The URL in each header
is documentation, not a fetch instruction.

Fetched https://www.speleotrove.com/decimal/dectest.zip, the successor location
of the referenced http://www2.hursley.ibm.com/decimal site. Compared every line
of both members against the samples. Only the copyright/contact/documentation
headers and version (2.59 versus 2.62) differ; all arithmetic rows and context
settings agree. No payload or obfuscation was found. External hostile labels
on these data files are unsupported; parent-archive label propagation or corpus
contamination is a possible explanation, but their actual source is unknown.

Fetched the official release from:
https://github.com/xmrig/xmrig/releases/download/v6.26.0/xmrig-6.26.0-linux-static-x64.tar.gz
The archive SHA256 is:
fc6f8ae5f64e4f17481f7e3be29a1c56949f216a998414188003eae1db20c9e5
This agrees with the asset digest published by the project's release page.
The enclosed xmrig is 8,350,992 bytes, SHA256:
b20f39fc00d242e706b6c30367ad811c676e0575050a4ec2f30104b696944b49
The sample's first 8,350,992 bytes are exactly equal to that executable.
Its only addition is a 64-byte binary trailer after the section-header table.
No ELF header, program header, mapped code, data, or constructor was changed.
The trailer is outside the loadable regions; stock XMRig has no activation or
self-overlay-reading path for it. Do not infer a payload from entropy alone.

Used rizin disassembly and source comparison against the v6.26.0 source archive
to trace the relevant paths, rather than relying on the product strings:

- Entry 0x40e5f3 passes main 0x40d280 to the static C runtime. main constructs
  Process (0x459d30), dispatches help/version (0x458c60), or constructs App
  (0x501040) and calls App::exec (0x501650).
- App::exec checks controller readiness. Its failure branch 0x5017a0 prints
  the configuration error and returns 2. Success follows the configured
  background, init, dry-run, controller-start and libuv-event-loop paths.
  This agrees with src/xmrig.cpp and src/App.cpp from the official source.
- Stratum share submission at 0x49e261 constructs a mining.submit request.
  Pool login, share processing, RandomX/CryptoNight code, developer donation,
  optional HTTP API, CPU discovery and hugepage/MSR tuning implement the miner's
  stated function. No extra wallet, attacker endpoint, persistence installer,
  credential theft, or Mirai scanning/attack dispatcher was added.
- References to /dev/mem at 0x525d51 and 0x525fdb belong to DmiReader's SMBIOS
  fallback. DmiReader_unix.cpp reads firmware tables through sysfs or physical
  memory and decodes hardware records. A path reference does not prove dumping
  credentials; the previous T1003 mapping was unsupported.
- At 0x605236 the MSR initializer attempts the allow_writes setting, then on
  failure 0x605250 passes /sbin/modprobe msr allow_writes=on > /dev/null 2>&1
  to the static system() implementation (0x9c4b84). This matches Msr_linux.cpp.
  It requires existing OS permissions; it is ordinary CPU tuning, not an
  escalation exploit. The previous command matcher missed its absolute path.
- The native dependencies and their strings are part of the exact official
  executable: libuv process/network helpers, OpenSSL TLS/crypto and hwloc
  topology discovery. Generic execve, kill, UID/GID, proxy and cryptography
  capabilities are not evidence that this program is a backdoor.

XMRig is often deployed without authorization in mining incidents, which can
explain miner AV signatures and this renamed artifact's hostile provenance.
The supplied standalone bytes do not establish an unauthorized installation.
The basename alone does not establish Mirai or cryptojacking.

Trait changes and controls
=========================

Moved mem/read/dump::dev-mem to fs/path/device/special::dev-mem-path, retaining
the ELF/shell/Python and Linux scope and notable severity. Removed the unsupported
access/dump description, credential mapping and unrelated library downgrade.
Added a word boundary to reject /dev/memory and /dev/member. The other three
atoms and memdump-ref composite in the source file remain unchanged. Audited
exact and ancestor YAML references: no consumer selected the removed dev-mem
atom, dump directory or read directory. A broad memory selector in the Empire
identity rule was also reviewed. Its Windows/PowerShell scope cannot overlap
the moved Linux ELF/shell/Python atom; effective matching is unchanged.

The destination is the existing leaf for special-device pathname observations;
this is a path, not an established physical-memory read. Its adjacent storage,
terminal and kernel-device leaves describe different device resources.

Expanded the existing os/kernel/module::modprobe-cmd matcher to recognize
standard /bin, /sbin, /usr/bin and /usr/sbin paths, preserving its types,
platforms, criticality and exclusions. Named its evidence as command text.
No separate miner-specific matcher or filename exemption was introduced.
Audited its linux-kmod-load and OpenWrt objective consumers: their additional
attack-specific required legs remain unsatisfied by ordinary XMRig.

Control files are static analysis fixtures; never execute them:
- absolute-modprobe.sh: both the module command and /dev/mem path must match.
- usr-modprobe.sh and bare-modprobe.sh: the module command must match.
- near-miss.sh: neither trait may match the similar program and path names.

Both decimal files retain their accurate corpus/documentation observations.
No hostile or suspicious traits are justified for any of the three samples.

Verification: all four focused controls passed using cleave test-rules.
Re-ran atomscan on all three supplied samples after the YAML changes. The
miner fires the corrected notable device-path and modprobe observations; the
old dump observation is absent. Every sample has zero hostile and zero
suspicious findings.
