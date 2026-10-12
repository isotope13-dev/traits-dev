# Encoded stealth-flag controls

The `encoded-stealth-*` npm traits searched every decoded layer, so a long
minified line carrying unrelated `\uXXXX` escapes Unicode-decoded wholesale
and a plaintext `--no-save` argv nearby counted as "encoded stealth". They
are now base64-only, matching the sibling `encoded-npm-install` leg.

`stealth-positive.js` hides both flags in a real base64 blob and still
matches; `stealth-nearmiss.js` passes the same flags as plaintext argv and
matches only the honest plaintext `npm-no-save-option` capability. Cases
checked with `cleave --traits-dir . --json` and assertions over emitted IDs.
