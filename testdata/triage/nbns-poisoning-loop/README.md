# NBNS spoof loop without the reflection half

Regression coverage for the remote-relay second review: that skeleton
poisons name resolution (NBNS answer bytes, transaction-ID walk, paired
`-lt 255` brute-force loops, socket send) without the local SMB reflection
half, so `nbns-poisoning-loop` reads suspicious while
`nbns-poisoning-for-ntlm-reflection` stays absent (1 hostile + 2
suspicious overall, anchored by the relay-execution hostile).

Controls are synthetic technique variants, not sample bytes:

- `positive-spoof-loop.ps1`: renamed loop variables and a while-loop
  shape fires the loop composite but not the reflection hostile.
- `negative-probe-loop.ps1`: paired loops and a send over a generic
  probe packet (no NBNS bytes, no transaction-ID assignments) fires
  neither.
- `staged-no-delivery.ps1`: NBNS bytes, transaction-ID walk, and paired
  loops but no socket send fires only `nbns-poisoning-staged`; the
  delivery rule stays silent via its send-leg suppressor.

Run `python3 testdata/triage/nbns-poisoning-loop/check.py`. It stages
copies into a temp dir before scanning (any path under this repo's own
`testdata/` tree matches the harness test-presence markers); `make
validate` does not execute it.
