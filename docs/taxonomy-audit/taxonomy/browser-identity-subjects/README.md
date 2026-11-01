# Browser identity and request evidence

Nine rules left the legacy browser leaf. The exact `/api/activities` literal
is a URL route observation; it does not establish an upload and no longer
inherits a transfer attack annotation. Four browser-account identity transfer
composites are classified by the information they collect. Two textarea
collection/upload composites are under captured input, and the remotely
selected request tap is under activity.

The Discord composite requires existing Discord exfiltration evidence, a file
form field and cookie permission. It does not require course content, so its
ID and description describe those actual conditions instead. Its predicates,
exceptions and severity are unchanged.

[moves.json](moves.json) records the original rules and rewritten consumers.
Run `uv run docs/taxonomy-audit/taxonomy/browser-identity-subjects/check-moves.py`
to compare the relocated predicates and effective defaults with that inventory.

The two textarea rules and the token-reference rule have also been renamed to
avoid implying quiz content or a token-store scan that their predicates do not
require. The new account-identity leaf contains four rules; all destination
leaves are below 80 rules.

`make validate` passed after the moves and renames: 1,927 hostile, 1,774
suspicious, 8,883 notable and 1,336 baseline fixtures.
