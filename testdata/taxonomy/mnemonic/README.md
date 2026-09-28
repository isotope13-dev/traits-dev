# Mnemonic capability and source controls

Run `python3 scripts/check-mnemonic-routing.py`. Fixtures are copied to temporary
paths and scanned. **Never execute them.** `cases.json` records finding-level
expectations, not whole-file risk classifications.

The controls separate mnemonic handling from generic wordlists/PBKDF2, recovery
UI from export, and keypair generation from phrase generation. They preserve
WIF and phrase source clues in existing consumers and exercise the 4 KB
weak-randomness proximity boundary. Local seed assembly must not be mistaken
for file targeting simply because several UI atoms match.

The wordlist-fetch positive uses a literal URL. The existing fetch atom does
not accept every indirect variable name, and the composite establishes nearby
fetch/path evidence rather than exact URL data flow. That limitation is recorded
in the audit rather than hidden by changing the matcher.
