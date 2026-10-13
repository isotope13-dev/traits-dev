# Parser test-corpus fixture context

Regression coverage for the saferwall/pe second review: that library vendors
password-protected ("infected") malware PEs under `test/` as parser fixtures,
and the inherited findings convicted the library itself (1 hostile + 14/15
suspicious on each of pe@v1.5.2 and pe@v1.4.7; now 0 hostile + 1 suspicious).

All three controls share one Shikata Ga Nai stub carrier (a 2012 specimen,
112,387 bytes, live bytes but inert as data):

- `corpus-direct.zip` → `test/direct-stub.exe`: single nesting keeps the
  member path visible, so the file-scoped `unless:` removes the finding.
- `corpus-nested.zip` → `test/nest.7z` (password `infected`) →
  `nested-stub.exe`: double nesting strips ancestor directories from the
  member path, so only the `scope: archive` `downgrade:` applies and the
  finding survives softened to notable at every level.
- `plain-stub.exe`: same bytes outside any fixture directory still convict
  at suspicious, proving the context moved and not the matcher.

Run `python3 testdata/triage/parser-test-corpus/check.py`. It scans this
directory with the local traits tree (the plain control by relative path,
so its location stays outside any fixture dir); `make validate` does not
execute it.
