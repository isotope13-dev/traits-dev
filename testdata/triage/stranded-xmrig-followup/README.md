# XMRig SFX member follow-up

The archive remains confirmed malware. Each member was recovered with bsdtar,
scanned, and examined independently. The executable and driver are byte-identical
to the official XMRig 6.25.0 Windows x64 release fetched with Forager. Their
hardware tuning, mining, cryptography, and vulnerable-driver findings remain.
The customized batch supplies the payout wallet for silent SFX activation.
Owner consent and the original distribution lure are unavailable.

| Artifact | Judgment | Hostile before/after | Suspicious before/after |
|---|---|---|---|
| WinRAR SFX | Confirmed MALICIOUS | 3 / 3 | 0 / 0 |
| `1.bat` | MALICIOUS | 0 / 0 | 0 / 0 |
| `xmrig.exe` | BENIGN | 0 / 0 | 0 / 0 |
| `WinRing0x64.sys` | BENIGN | 0 / 0 | 0 / 0 |

New notable detections cover HAL bus-configuration reads/writes, buffered port
I/O instruction sequences, and kernel I/O-space unmapping. Physical mapping
and unmapping observations moved from memory protection to their operation
homes. The existing union retains its exact alternatives under `mem/combined`;
its name now includes unmapping. Exact consumers and the broad memory selector
retain the original observation set. The generic T1055 mapping on these
capabilities was unsupported: they do not require process injection.

`ExitThread` moved from thread creation to termination. Its locale-exit consumer
retains the exact matcher. Creation directory selectors no longer accept thread
exit as creation evidence. The FLS/exit control demonstrates the old unsupported
claim, while the FLS/CreateThread positive still fires. Argon2 and
EVP_PKEY_derive references, and the existing KDF union, are notable crypto
observations; descriptions state references rather than proven execution.

`migration.json` accounts for the moves. `review.json` records hashes, markers,
disassembly observations, normalized before/after results, and limitations.
The legacy XOR/add mapping token is preserved unchanged; it was rejected by
the string extractor in both baseline and current minimal controls, so it is
not presented as a newly successful detection.

There are no material attack losses. A different malicious SFX fixture retains
all three hostile detections. Some compact-output findings disappear because
the engine filters any/needs-one unions and unreferenced baseline atoms;
explicit `test-rules` traces confirm the mapping union and relocated exit
matcher still match. Final comparisons bypass report caches. Initial cached
reports included extra display-level observations.

The standalone launcher has ten notable findings and no independently
matchable hostile mechanism beyond its configured mining task. Its silent
activation belongs to the containing SFX. Its bytes contain no separate
persistence, evasion, theft, download, or cleanup behavior to support three to
five hostile rules. ML remains at calibrated level -1/confidence 0 for both
malicious artifacts; the archive still has three hostile rule findings. The
engine reports a v18 feature specification where v21 is expected.

Verification: 23 new inert controls, six existing member controls, eight
existing memory attack/near-miss controls, seven effective matcher/scope moves,
and before/after member/container rescans. No sample was executed.

Run the focused controls with:

```sh
python3 testdata/triage/stranded-xmrig-followup/check.py /path/to/scratch/controls
```

Recovered bytes, official release/source downloads, `.forage.json` provenance,
decoded strings, matcher traces, and full scans remain under the task's
`scratch/d220-review` directory. Verdict markers sit beside the listed archive
and each extracted member, outside the traits worktree.
