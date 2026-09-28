# Bind identity encoding to the requested HTTP hostname

The old `dns-exfil-curl-hex` combined a variable-shaped curl URL and an independent
line-start `xxd -p` occurrence. An unrelated hex dump could therefore support a
hostile verdict, while an actual single-line `hostname | xxd -p` pipeline was
missed. Broadening the hex atom alone would amplify that false inference.

## Canonical behavior and objective

`micro-behaviors/communications/http/request/url::shell-identity-hex-hostname-request`
now recognizes consecutive shell statements with a bound relationship:

1. Capture the output of `hostname`, `whoami` or `pwd` piped into `xxd -p`.
2. Use that same variable as the leading hostname label of the next curl HTTP(S)
   request. Both `$name` and `${name}` forms are supported.

The query requires the command substitution and pipeline structure, matching
variable captures, a double-quoted interpolated URL, and statement adjacency.
It allows the documented simple curl flags. An intervening reassignment, a
single-quoted literal, a different variable, or a visibly shadowed command does
not qualify. File-wide exclusions cover function definitions and alias settings
for the relevant commands, plus background assignments whose child-shell value
would not update the requesting shell.

The canonical `hex-encode-xxd` atom now recognizes parsed commands with `-p` as
the first argument, including pipelines and redirections, instead of requiring
line-start text. It excludes visible xxd functions and aliases. The bound-flow
observation and this independently reusable encoding observation are both notable.
The objective retains the existing hostile level
under `objectives/exfiltration/http/hostname::shell-hex-identity-transfer`, now
requiring both observations. The HTTP hostname is the observed transport
field; the source does not prove that a DNS query actually occurs. The original
unencrypted-DNS ATT&CK suffix is removed rather than asserting an unproven
protocol/encryption mapping. No historical DNS alias remains.

Two install-hook composites are retired. They merely repeated this hostile
verdict alongside reconnaissance observations, did not require an install hook,
and did not establish that additional gathered fields were transmitted. Their
primitive findings and the canonical transfer objective remain available; no
separate installation feature is justified by those predicates.

The generic encoder's other consumers were audited before broadening it.
`rust-encrypted-dropper-builder` retains its separate executable-path,
encryption-documentation and compilation conditions. The unused
`stealer/system-info::shell-dns-exfil` is retired: identity, curl and independent
encoding do not establish DNS transfer, and its unsupported inference would
otherwise expand alongside the encoder. The canonical bound transfer covers
the tested actual hostname-egress mechanism.

The repeated curl-definition exclusion is now one canonical
`data/source/function/names::shell-curl-function-definition` observation, reused
by the four consumers. Function definitions and command invocations remain
different facts; the shared definition guard must not be merged into a curl-call
matcher. The validator's cross-type canonicalization now preserves the function
kind discriminator, with a regression checking that call-versus-text duplication
is still reported while a definition is excluded from that warning.

The [ten-entry ledger](shell-host-flow-mapping.json) records both new atoms,
the revised/relocated objective, encoder correction, three retirements and three
existing-consumer guard rewrites. The
[consumer audit](shell-host-flow-consumer-audit.json) covers exact and ancestor
support, including removal of unsupported installation and DNS classification.

## Regression matrix

Ten inert archives contain ordinary `client.sh` members; none is executed:

| Case | Transfer objective |
|---|---|
| Single-line identity/xxd pipeline | Required |
| Multiline identity/xxd pipeline | Required |
| Renamed binding, braced expansion and curl flags | Required |
| Independent hex dump and regional service request | Forbidden |
| Reassignment between production and request | Forbidden |
| Different variable in requested hostname | Forbidden |
| Single-quoted literal dollar text | Forbidden |
| Function replacing xxd | Forbidden |
| Alias replacing xxd | Forbidden |
| Background assignment | Forbidden |

The initial eight-case read-only comparison reproduced the unrelated-hex false
positive and the single-line false negative. The final fixture set adds braced
expansion and alias cases. All ten pass the checkout suite; installed atomscan
is checked independently. Reports and snapshots are in
`/tmp/taxonomy-shell-host-flow/`.

The rebuilt checkout passes **1,781/1,781 fixtures**: 268 hostile, 485 benign,
175 does-nothing, 45 drop-exec, 571 supply-chain, 66 impact-wipe, 82 obfuscation,
24 reverse-shell and 65 simple-stealer. All **14 cross-type validator tests**
pass, including the new definition/call distinction. Installed atomscan separately
verifies the ten-case matrix, with no suspicious/hostile findings in the seven
negative controls and canonical hex-encoding findings in all three positives.

Structural inventory reports **168 oversized directories** and zero mixed nodes.
Strict validation has no remaining issue introduced by this cohort; it still
reports the cap debt and separate PowerShell, WASM, Silver Sparrow description/
regex failures and two excessive-suppression rules. Concurrent Chopper and
Silver Sparrow definition changes are excluded from the ten-entry ledger and
listed in the temporary `unrelated.json`; the 58 consumer decisions cover this
cohort's old and new directory support. The entire migration remains incomplete.

## Scope and remaining work

This is bounded source-local analysis, not whole-program taint tracking. It
currently requires adjacent top-level statements, the specific producer commands,
`xxd -p`, and the supported double-quoted URL shape. Other shell encoders, function
bodies, intervening transformations, and indirect command resolution require
separate grounded coverage; a fixture pass does not prove those variants.
Visible shadowing is excluded conservatively, not resolved through arbitrary
sourced code or runtime environment changes.

The generic encoder deliberately recognizes parsed `xxd -p` command syntax;
other option ordering, executable spellings and encoders remain separate coverage
questions. Its broad directory consumers are included in the audit, because they
gain actual pipeline encoding and lose incidental line-start text. Remaining
legacy DNS and HTTP co-occurrence rules still require the same relationship and
placement review.
