# Compiled base64 execution

`base64.scpt` hides a shell command in a base64 string literal, then pipes the
decoded text to `sh`. The command only prints `SCPT_BASE64_OK`; the encoded
execution pattern is deliberately suspicious. Do not run the fixture.

Compile and inspect:

```sh
osacompile -o testdata/obfuscation/applescript/base64.scpt testdata/obfuscation/applescript/base64.applescript
cleave strings testdata/obfuscation/applescript/base64.scpt
cleave facts testdata/obfuscation/applescript/base64.scpt
```

Use a cleave build linked against the updated filefacts parser. Both commands
expose `printf '%s\n' 'SCPT_BASE64_OK'` at the encoded literal's offset, `0x29a`.
Facts labels it `scpt-base64`; strings carries `["scpt", "base64"]` provenance.
The original UTF-16BE base64 literal remains available.

This fixture covers the gap between parser-extracted literals and stng's raw
text scan. Filefacts now feeds stored and reconstructed SCPT literals through
stng's shared decoders. Decoder and CLI regressions use copies of this compiled
fixture; no test executes it.

The trait `micro-behaviors/data/decode/base64::base64-decode-piped-shell` should
be suspicious. It describes the execution pattern, not the decoded command's
intent. Data-only decoding and hardware inventory must remain below suspicious.

Run the static shell and compiled AppleScript controls with the updated build:

```sh
CLEAVE=../cleave/target/debug/cleave python3 scripts/test-base64-shell.py
```
