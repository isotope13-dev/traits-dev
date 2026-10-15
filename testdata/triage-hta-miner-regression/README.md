# HTA downloader / encoded-miner triage regression

Fixtures for the October 2026 triage of three VirusShare HTML samples:

- `hta-chr-shell-launch.hta` models the HTA downloader (VBScript resolves
  `Shell.Application` from `Chr()` codes, launches via `ShellExecute`).
  Must fire both new hostile composites.
- `hta-plain-controls.hta` is a benign admin-style HTA (literal ProgID,
  `Run` instead of `ShellExecute`, no `Chr` density). Must fire neither.
- `coinhive-unescape-miner.html` models the cryptojacking injection
  (`document.write(unescape(...))` decoding to `new CoinHive.User(...)`
  plus `miner.start()`). Must fire both new hostile composites.
- `blog-ad-controls.html` models the benign blog (ad `document.write`,
  plain `createElement('script')`). Guards the `svg-script-element-create`
  tightening: the plain atom still fires, the SVG atom stays silent.
- `stylesheet-credential-controls.html` is theme CSS listing
  `input[type="password"]` / `input[type="email"]` selectors with no input
  tags. Guards the `password-then-email-inputs` anchoring.
- `form-pair-controls.html` is a real password-then-email form, the
  positive control the anchoring must keep.

Run: `python3 testdata/triage-hta-miner-regression/check.py
[--cleave-output.json]` (accepts a saved scan to skip re-running cleave).
Fixtures are scanned as copies outside the repo because some legs carry
test-directory exclusions on repository fixture paths.
