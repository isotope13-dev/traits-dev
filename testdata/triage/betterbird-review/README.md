# Betterbird and ltidisafe second review

Betterbird 153.1.0 is a Thunderbird/Gecko mail client. Its application metadata,
compiled native runtime, and packaged JavaScript agree on this identity.
The built-in Thundermail extension performs account authentication and
user-requested encrypted file sharing. Message origins and send.tb.pro hosts
are checked; tokens and encryption keys are handled as part of that workflow.
No covert installation payload, credential theft, or concealment was found.

Native disassembly shows `should_hide` being constructed as a Rust field name,
not an exported directory-filter hook. Ordinary `readdir`, `dlsym`, and `write`
imports plus procfs strings therefore do not prove a rootkit. Hook verdicts now
also require explicit hiding evidence. A callable should_hide symbol is a
neutral observation; a saved original_readdir provides additional context.
The ELF controls contain section data and symbols but no executable segments.

`downloadModel`, WebRTC RELAY, navigation STOP_ALL, the Microsoft software
renderer, normal temporary paths, and a canvas context-loss warning are not
remote commands, botnet opcodes, VM detection, hidden staging, or ransom threats.
The positive controls retain the specific command, hide-action and data-loss
patterns. Structured bookmarks members exclude preference-key lookalikes.

The archive loader composite previously pooled unrelated modules. File scope
prevents this, and suspicious severity reflects concealed loading without
claiming a proven hostile payload. High-entropy add-on blocklist Bloom filters
are measurements, not crypters. Ordinary declarations, URL checks, UI messages,
record fields, decoding, file access, evaluation and cryptography retain neutral
notable signals in their capability or metadata homes. Consumer references are
updated, including same-leaf references. Broad directory membership was reviewed
alongside exact references; moving neutral evidence out of objectives intentionally
removes it from attack-only selectors.

Existing leaf boundaries were reused. Cap review moved multiply/rotate arithmetic
out of dispatch, JSON serialization out of generic record schemas, URL construction
out of host identity, grammar tables out of package lifecycle, and generated-source
markers out of filename properties. No count-driven taxonomy split was introduced.
The bare santa keyword was removed: it matched a Matrix emoji label and supplied
no filename-selection evidence. Sensitive-record terms now require document paths.
Microsoft application-policy certificate OIDs and enrollee flags are neutral
certificate capabilities; the exploit composite retains its impersonation gate.
HTTP request body writes are distinguished from file-stream writes, and attack
consumers require the HTTP signal rather than treating file output as exfiltration.

ltidisafe 3.6.6 remains malicious. Its quiet npm preinstall hook executes test.js,
which hex-encodes the username, hostname and home directory and passes each as
an OAST hostname label to an HTTP network-speed helper. The helper performs the
actual request. Interface addresses are computed but not transmitted; commented
uptime collection is inactive. Existing flow-aware rules already provide two
hostile findings, so no additional sample-specific signature was added.

Run `python3 testdata/triage/betterbird-review/check.py` and
`python3 testdata/triage/hex-identity-benchmark/check.py` for the regression controls.
The first runner generates inert ELF files and scans isolated copies so testing
path exclusions cannot silently turn positive controls into false negatives.
