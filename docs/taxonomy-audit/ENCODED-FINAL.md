# Retiring the encoded reverse-shell leaf

The last three rules in `reverse-shell/encoded` do not establish a relay. This
batch removes that leaf and audits the associated bind-shell label, decoded
imports and interpreter reference. The [eight-entry ledger](encoded-final-mapping.json)
records effective definitions, destinations and intentional changes.

## Placement and evidence

A Python file that merely decodes and prints `import os`, `import socket` and
`SHELL = "cmd.exe"` reproduced the hostile socket-shell verdict. A PHP file that
prints encoded option labels and separately evaluates `return 2 + 2;` reproduced
the packed bind/back-connect-shell verdict. Neither has a network connection or
shell process. Import names, labels and evaluator presence cannot establish their
relationship.

- The two hostile composites are retired. There are no remaining consumers or
  parent-level aliases for them.
- Two Base64/reversed-ROT13 shell labels move to
  `metadata/file/string/security`, alongside other security vocabulary. Their
  exact matchers, file scopes, exclusions and confidence are preserved; their
  criticality is notable and irrelevant attack annotations are removed.
- The encoded `cmd.exe` reference moves to `process/interpreter/shell`, preserving
  its matcher, scope, exclusions and confidence at notable. The existing Windows
  resource-loader consumer follows its canonical ID.
- Two decoded import observations and their roll-up move to
  `metadata/import/package`, at notable. The remaining payload consumer uses the
  new canonical system-import reference. The atoms now require a module-name
  boundary: `import osquery` is not evidence of an `os` import, nor is
  `import requests_cache` evidence of importing `requests` itself. These are
  descriptions of encoded import text, not proof of executed imports.

`TAXONOMY.md` closes the encoded objective namespace and documents the vocabulary,
import-metadata and mechanism boundaries.

## Verification

The new benign archive contains the Python stored-text and PHP label controls.
Its score falls from **202 to 12**; members fall from **158 to 9** and **163 to 6**.
It is capped at 15, requires the neutral destinations, and forbids both reverse-
shell and bind-shell prefixes. The validator also rejects suspicious/hostile
intent findings on its members.

The new positive archive wraps the existing direct Python stream relay in Base64,
with `cmd.exe` as its shell. The decoded child still matches
`stream-bridge::python-popen-socket-stream-relay`; the archive scores **160** and
its decoded children **125–126**. A plain fixture under testdata was suppressed
by the existing test-directory exclusions, so the archive member exercises the
behavior without changing those exclusions. The positive requires stream-bridge
coverage and retains a score floor of 100 and at least one hostile finding.

The full soft run passes **1,667/1,667 fixtures**. Strict validation still reports
**176 oversized directories**. The ledger verifies against effective current
rules, no migrated IDs remain in dependencies, and there are zero mixed rule
directories. Destination counts are security vocabulary 22, import/package 57,
and interpreter/shell 11, all within the combined cap.

## Coverage gap found during the audit

An independently generated PHP descriptor relay wrapped in
`eval(base64_decode(...))` is decoded and typed as PHP, but its decoded child has
**zero AST calls**. The child lacks `<?php`, as a valid PHP eval body normally
does. The current filefacts language configuration uses
`tree_sitter_php::LANGUAGE_PHP`, whose document grammar treats this body as text.
The `fsockopen` call fact is consequently absent, and the existing descriptor-
relay composite does not fire. Neutral textual socket/descriptor observations
and generic encoded-loader detections still fire; the tested wrapper scores 153,
but that is not evidence of mechanism coverage.

Reproduce by taking `testdata/reverse-shell/revshell.php`, removing its opening
and closing PHP tags, Base64-encoding the body, and putting the encoded literal
inside `<?php eval(base64_decode('...'));`. Scan it; do not execute it. The child
is reported as `##script@6`, with AST call count zero. Local reproduction and
scan output are `/tmp/taxonomy-encoded-last/encoded-php-descriptor-relay.php` and
`/tmp/taxonomy-encoded-last-before.json`.

This is an existing decoded-source parsing gap, not coverage supplied by the
retired label rule: that reproduction contains neither label. Fixing it should
select the PHP statement/snippet grammar for known extracted eval bodies,
without interpreting arbitrary tagless PHP/HTML documents as executable code.
It needs parser and end-to-end regression tests. This batch makes no parser
change and does not claim equivalent coverage for every historical packed sample;
the particular packed PHP and jsonschema samples mentioned in the retired rule
comments were not available in the located fixtures.

The encoded leaf is retired, but the broader cap migration and sibling audits
remain incomplete. Continue the bounded cross-domain cap cohorts while tracking
this parser gap and the earlier overlapping interactive-flag evidence issue.
