# Encrypted staging retirement: remaining PowerShell rules

The final twelve rules moved out of legacy encrypted staging:

- Base64 literals, Base64-encoded XOR/modulo observations and Decrypt-AES name
  observations moved to encoding and function-name metadata. Name counts do
  not establish decryption or chunk accumulation.
- Batch Base64/decryptor, join/crypto, Base32/AES, AES/write/hidden and
  Base64/transform combinations moved to decryption profiles. Encoded XOR,
  file-write and hidden PowerShell clues moved to file-write context. They do
  not by themselves identify staged payload execution.
- The inline `Invoke-Expression` of a transform, with AES and decoder clues,
  moved to `execution/payload/script-eval/transformed` and remains hostile.

The original conditions, explicit file types, platform scopes, count and
proximity thresholds, confidence and suppressions were preserved; IDs and
references were redirected. Names, severity and unsupported attack annotations
were corrected where the former description overstated the evidence. A
synthetic positive PowerShell script matched the inline AES evaluation rule;
the same script without `Invoke-Expression` did not match. This exercises the
execution rule, not every migrated profile.

The adjacent crypto/decrypt directory was split from 88 to 72 direct rules:
AES-GCM, AEAD tag, Web Crypto, NSS and triple-DES observations moved to their
algorithm or provider subjects. Web Crypto has a separate provider namespace,
so existing AES-plus-Web-Crypto clauses remain distinct. The other moved AES
observations now satisfy six existing positive AES-directory references; this
can broaden those consumers. The file string-population profile directory was
split from 85 to 73, with 12 binary-specific rules in `binary-strings`. Exact
and cross-directory local references were redirected. No directory-wide
references to either former source directory were found.

No YAML rules or live YAML references remain under the legacy encrypted
staging namespace; the empty directory was removed. Other legacy staging
categories remain.
