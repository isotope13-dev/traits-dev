# C mislabeled-good review, 2026-11-04

The input is a snapshot and is not removed by `hopper mv`. Of its 40 files,
33 are single configuration macro definitions. They contain no implementation,
including the `CONFIG_TEARDROP` and `CONFIG_NEWTEAR` definitions. Atomscan
reported no suspicious or hostile traits for them. The declaration-only
`43e83cee58d4` header likewise has no implementation; after correcting the
identifier-based findings, atomscan reported no suspicious or hostile traits.
Hopper confirmed all 34 already have the good label (34 no-ops).

The remaining `290c82299346` header implements general Windows API hooking and
DLL injection. Its suspended-process injection preserves the original entry
point and is not established as hollowing. It is good as a general-purpose
utility: API-hooking observations are notable, and the unusual suspended
process/memory staging remains one suspicious finding. Hopper confirmed the
sample already has the good label (no-op).

The `25e6e956efb5` eBPF SSH backdoor changes user-space reads of account and
authorized-key data following a source-port trigger. Atomscan now reports
hostile findings for the two branches in separate directories. The prior
sudoers finding was unsupported by its matcher. Hopper moved the sample from
good to bad; the triage copy was relocated to `/tmp/triage/misplaced-bad`.
The `ea4ccf74ada4` controller supplies a backdoor public key, trigger ports and
altered account/password data. Atomscan reports hostile account-backdoor and
SSH-backdoor controller findings. Hopper moved it to bad and the triage copy
was relocated to `/tmp/triage/misplaced-bad`.

The `3b693f3d1f10` eBPF controller loads PID-hiding code and supplies its own
PID and a user-supplied name to a files-to-hide map. Atomscan reports hostile
process and file concealment findings. Hopper moved it to bad and the triage
copy was relocated to `/tmp/triage/misplaced-bad`.

The `5bc5e02d69fe` implementation contains a ComputerDefaults class hijack,
keyboard capture, and a regex-gated clipboard replacement helper alongside
cryptocurrency address patterns. Atomscan reports hostile UAC-bypass and
crypto-clipboard findings. Hopper moved it to bad and its triage copy was
relocated to `/tmp/triage/misplaced-bad`.

The `bf44aeaeaba7` program collects Discord tokens from local storage, decrypts
them and posts token data. Its browser password/cookie collection calls are
commented out, although functions for posting those vectors remain. Atomscan
reports hostile token-recovery and upload findings in distinct directories;
Hopper moved it to bad and its triage copy was relocated. An unrelated
DOS-header-patching finding was a substring match on `ExeInfection`; the
identifier observation was corrected and no longer matches that longer name.

The focused `test-c-triage-evidence.py` regression checks declaration-only
handle references, DLL injection versus hollowing, and shadow versus sudoers
references. `make validate` passed after the rule changes. The 40-file scan
used slow local mode; its JSON is at `/var/tmp/c-good-scan.jsonl` for this
session and predates the fixes; individually rescanned samples are described above.
`test-ebpf-account-backdoor.py` checks both new backdoor branches and negative
cases without the write or targeted branch, and the controller's required key,
port, password-copy and map evidence. `test-ebpf-hide-controller.py` checks
the distinct process and file evidence. `test-native-clipper-uac.py` checks
clipboard and UAC evidence and negative cases. `make validate` passed.
After further tightening the clipboard matcher to require a differing
replacement address, its focused test and sample rescan passed. The unrelated
concurrent validation issue was fixed, and the latest `make validate` passed.
`test-native-discord-token.py` checks token-recovery and upload evidence and
the EXE identifier boundary.
