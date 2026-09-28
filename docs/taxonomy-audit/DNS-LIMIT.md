# A maximum-length assignment is not DNS truncation

The old `dns-label-truncation` searched only for `max_length=63`. It observed
neither truncation nor use of the setting. Combining it with a variable-shaped
curl hostname produced a hostile exfiltration verdict on a normal service request.

## Changes

- Preserve the assignment matcher under
  `metadata/file/string/limit::max-length-63-assignment`, named as assignment
  text and baseline. The exact number is a literal characteristic, not evidence
  of a meaningful executed capability. It may also occur in comments.
- Move the curl URL matcher to
  `communications/http/url/build::shell-curl-variable-host`, at notable. Its
  predicate and scope are unchanged. It matches a variable-shaped hostname,
  including quoted spellings; it does not prove expansion, collection or DNS
  exfiltration. The old description explicitly overclaimed DNS exfiltration.
- Retire `dns-exfil-curl-truncation`; the two observations do not establish its
  advertised relationship.
- Retire the resulting single-leg `dns-exfil-curl` roll-up. Its two install-hook
  consumers now reference the surviving `dns-exfil-curl-hex` directly. That
  composite's conditions and criticality are unchanged except for the canonical
  URL reference.

The [seven-entry ledger](dns-limit-mapping.json) records both moves, both
retirements and three consumer rewrites. The
[ancestor audit](dns-limit-ancestor-audit.json) records changed directory support.
No parent alias or directory exception is introduced.

## Evidence

`dns-service-limit.zip` contains an inert `client.sh` assigning `max_length=63`,
selecting the fixed region `west`, and requesting that region's service URL under
`.invalid`. Before, it produced a hostile truncation/exfiltration verdict. After,
its constant and URL observations remain without suspicious or hostile findings.
The fixture requires both neutral homes and forbids the DNS exfiltration branches.
No sample or control is executed.

`dns-host-label-egress.zip` contains an inert `client.sh` that obtains hostname
text, hex-encodes it with `xxd -p`, and places the resulting value in a curl URL
hostname. It requires a hostile finding from the surviving side-channel DNS
branch. Unlike the negative case, the source actually carries identity data
through the hostname.

The first positive spelling, `identity=$(hostname | xxd -p)`, exposed an existing
coverage gap: `hex-encode-xxd` is anchored at the start of a line, so it misses
this ordinary pipeline form. The final regression uses the equivalent multiline
pipeline. This is not evidence of comprehensive shell-pipeline coverage; the
single-line gap remains an explicit follow-up. The retained composite's effective
predicate comparison proves that this cohort did not introduce that gap.

Reports and snapshots are under `/tmp/taxonomy-dns-limit/`. Before/after scans
use installed atomscan; fixture gates use the sibling checkout engine.

The final checkout fixture gate passes **1,771/1,771**, including 478 benign
controls. Strict validation reports **168 oversized directories** and the
concurrent PowerShell description/regex-length and suppression-count failures.
Structural inventory finds zero mixed nodes. The effective-rule comparison
records exactly seven changes and 33 ancestor decisions, with no unrelated
definition changes in this cohort. Installed atomscan separately reports risk
2 and no suspicious/hostile findings for the service request, and risk 117 with
the surviving hostile hex-transfer finding for the multiline egress control.

## Remaining work

The retained hex-transfer composite still combines independent text observations
without binding the encoded output to the URL. A service script with unrelated
hex conversion is a needed negative control for its next revision. Audit the
shell command AST or a bounded data relationship before expanding the anchored
`xxd` matcher: broadening the atom alone would also broaden the hostile consumer.
The remaining `dns/prep` chunking and label-vocabulary entries, and overlapping
`dns/tunnel` versus `side-channel/dns` objective branches, remain open.
