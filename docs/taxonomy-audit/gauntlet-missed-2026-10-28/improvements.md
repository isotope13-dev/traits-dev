# Trait improvements from the reviewed Gauntlet samples

This pass addresses the three unresolved precision issues in the reviewed Python packages and two descriptions/matchers on the decoded JavaScript carriers. It does not complete manual review of all 140 samples.

## Claims now match their evidence

| Sample | Before hostile/suspicious | After hostile/suspicious | Correction |
|---|---:|---:|---|
| `pafex-2.3` wheel | 1/0 | 0/1 | Unsafe pickle loading and a late type check establish a dangerous loader, without proving a malicious serialized payload. Move the observation to unsafe serialization capabilities. |
| `workcalender` sdist | 0/2 | 0/0 | Keep the name, build-hook declaration, print-only test marker and contradictory publication claims as metadata. These do not establish an attack. |
| `moveworks_capi_starter` wheel | 0/3 | 0/0 | Keep dummy-summary, example-author and dummy-version statements in metadata; remove unsupported squatter/impersonation claims. |
| `6baed65e86355ac0.js` | 2/0 | 2/0 | Require executable XOR and immediate Function invocation. Describe the encoded execution mechanism instead of claiming an appended injection. |
| `0c76358cf582c52e.js` | 2/0 | 2/0 | Same independently checked wrapper mechanism and controls. |
| `resion-22.0.1` wheel | 4/1 | 4/1 | Control: known malicious config/persistence sample retains its findings. Its payload was previously decoded statically. |

Matchers and container scopes were preserved for metadata/capability relocations. The JavaScript changes intentionally tighten detection: the old injection rule omitted XOR, and the TextDecoder rule did not require invoking the constructed function. The renamed rule is `objectives/execution/interpreter/eval/dynamic::js-large-base64-xor-function-execution`.

## Verification

Fresh `atomscan --format=json --mode slow --analyze local --follow=none` scans use the workspace traits. Evidence summaries are in `/tmp/gauntlet-missed-review/improve-after.jsonl`.

The renamed JavaScript rule scored 7.2 precision in `cleave test-rules`. Both original carriers matched. A code variant with XOR removed, while retaining the original XOR text inside a comment, did not match. A comment-only copy did not match. A further control keeps construction of the Function but removes its invocation; both wrapper rules must reject it. Final assertions are saved in `/tmp/gauntlet-missed-review/improve-wrapper-checks.json`.

`RAYON_NUM_THREADS=8 make validate` passed after the final matcher changes: hostile 2797/2797, suspicious 1757/1757, notable 8441/8441, baseline 1316/1316. All five wrapper cases passed for both rules. Log: `/tmp/gauntlet-missed-review/improve-validation-final.log`. The worker limit controls scheduling and does not change validation thresholds. No thresholds or exception rules were changed. A redundant per-item `for: [pe]` declaration was removed from `windows-pe-ftp-php-gate.yaml`; the same scope is inherited from its file default.

## Remaining decoder limitation

A temporary `type: encoded` probe for the hidden security-check label did not match the original Base64/XOR carrier. The hidden iframe source has been decoded manually, but current generic encoded-string matching does not expose that label through both layers. No nonfunctional overlay rule was added. The evidence is under `/tmp/gauntlet-missed-review/probe-rules/` and the decoded stage files under the original hashes.

The separate native-binary review, including `My 2FA KeyX.exe`, and the unreviewed ledger rows remain open. These trait corrections do not resolve those verdicts.
