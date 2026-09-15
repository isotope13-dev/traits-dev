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

Current gap: filefacts recovers the base64 value as a UTF-16BE `scpt-literal`,
but the stng text view misses it and neither view contains the decoded command.
Parsed literals need to reach the shared string decoders, preserving their
source anchor and decoding provenance. Stng's base64 support alone does not
cover this path.
