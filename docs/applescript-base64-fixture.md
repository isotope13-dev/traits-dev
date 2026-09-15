# Compiled base64 execution

`base64.scpt` hides a shell command in a base64 string literal, then pipes the
decoded text to `sh`. The command only prints `SCPT_BASE64_OK`; do not run the
fixture.

Compile and inspect:

```sh
osacompile -o testdata/obfuscation/applescript/base64.scpt testdata/obfuscation/applescript/base64.applescript
cleave strings testdata/obfuscation/applescript/base64.scpt
cleave facts testdata/obfuscation/applescript/base64.scpt
```

The compiled fixture covers the gap between parser-extracted literals and
stng's raw text scan. Filefacts feeds stored and reconstructed SCPT literals
through stng's shared decoders; no test executes the fixture.

The trait `micro-behaviors/data/decode/base64::base64-decode-piped-shell` is
expected to be suspicious. It describes the execution pattern, not the
decoded command's intent.

Run the static controls with the updated build:

```sh
CLEAVE=../cleave/target/debug/cleave python3 scripts/test-base64-shell.py
```
