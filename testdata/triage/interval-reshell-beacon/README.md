# Interval re-executed dev/tcp shell beacon

Regression coverage for the fix-peer-deps second review: its `example.js`
demo hid a 30-second `setInterval` re-execution of a Base64-encoded
`/dev/tcp` reverse shell behind an otherwise legitimate peer-deps tool.
`node-interval-devtcp-shell-beacon` (hostile) binds the timer to the
encoded shell and its `child_process` execution, giving the package the
second hostile its verdict needs next to
`eval-decoded-devtcp-reverse-shell`.

Controls use synthetic payloads (different endpoint, port, interval, and
surrounding code than the sample), not its bytes:

- `positive-beacon.js`: timer + encoded shell + encoded `child_process`
  exec fires the beacon hostile.
- `negative-timer-only.js`: bare `setInterval` fires nothing ≥ suspicious.
- `negative-shell-no-timer.js`: encoded shell without timer or exec keeps
  the decoded-shell hostile but not the beacon rule.

`check.py` stages copies into a temp dir before scanning: any path under
this repo's own `testdata/` tree matches the harness test-presence
markers, which (correctly) suppress the encoded-shell legs the rule builds
on. The committed bytes are the test; the temp location is just scaffolding.
