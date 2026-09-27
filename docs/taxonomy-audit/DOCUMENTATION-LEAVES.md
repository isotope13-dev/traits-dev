# Documentation leaf-only repair

The live 2026-09-27 tree had nine rules directly in
`metadata/package/documentation/npm-readme-anomalies.yaml`, beside rule-bearing
children. All nine now have leaf homes; the parent file is removed.
[The effective-definition ledger](documentation-parent-mapping.json) records
all nine moves and one additional duplicate merge, including inherited scopes.

| Required observation | Canonical leaf | Final combined count |
|---|---|---:|
| Manifest description discloses CTF purpose | `metadata/package/description/disclosure` | 36 |
| Exact README.md basename | `metadata/package/documentation/source` | 27 |
| Prose claims inertness or confusion prevention | `metadata/package/documentation/claims` | 10 |
| npm removal statement or advisory reference | `metadata/package/documentation/security-advisory` | 13 |

No new directory, cap exemption, parent alias, or language-based partition was
introduced. TAXONOMY.md documents the boundaries among these existing leaves.

## Intentional detection changes

- A CTF description and an inert-placeholder claim are neutral notable facts.
  They do not establish a supply-chain attack or deception. Removed the CTF
  attack tag and renamed the two misleading `misdirection`/`decoy` composites.
- CTF now requires a complete word. `factfinder` is a negative control for the
  old substring match. Actual CTF descriptions retain their factual signal.
- The README matchers previously inherited `for: [package.json]`. They now also
  admit Markdown and text; README conjunctions can actually match documents.
  Prose atoms describe statements in text, not an unverified document role.
  Composites claiming README context explicitly require its basename.
- Literal regexes became case-insensitive substrings without changing their
  accepted text. The duplicate removal statement formerly in
  `metadata/package/freeform` merged into the canonical advisory atom, with
  the higher existing confidence (0.99), the union of file-type scopes, and
  case-insensitive matching. Its explicit composite consumer was updated.
- Existing exclusions on the placeholder composites are retained.

Directory references are not aliases: `documentation/` loses the manifest CTF
observation and gains no substitute for it. The README rules remain descendants
of the same parent. `freeform/` loses the removal statement; a bare removal
notice should not establish that unrelated free-form package context. The
explicit npm security-holder composite still references the canonical statement.
The existing freeform title/advisory-link predicates are not identical matchers
(the link requires `www.`); their remaining placement merits a later coordinated
freeform audit rather than copying them into the advisory leaf.

## Platform-scope conflict and validator follow-up

**Resolved in the subsequent [stream/scope batch](STDIO-STREAM-OBSERVATIONS.md):**
platform count is now a non-blocking review across all tiers, with the old
directory exemptions removed. The discussion below records the conflict that
motivated that change; the preserved documentation scopes now pass strict scope
validation. The directory cap remains blocking.

The old six-platform list included both `unix` and its `linux`/`macos` members.
It is now the equivalent `[unix, windows, android, ios]`. The engine currently
does **not** include Android/iOS in its Unix umbrella. Dropping them would narrow
explicit platform-filtered scans, and splitting identical observations by OS
would reproduce the organization problem this migration is meant to remove.

Strict validation flags six atomic rules for its separate four-platform limit.
This was already inherent in the parent definitions and is now explicit in the
leaf migration. No platform exception was added and coverage was not narrowed.
Review that heuristic for format-defined metadata: the number of OS platforms
is not evidence that a manifest field or documentation statement is imprecise.
This is separate from the required 85-rule directory cap, which remains strict.

## Verification

Four benign controls cover actual README claims, an npm-removal statement,
CTF disclosure, and the `factfinder` counterexample. Each has a score cap of 5;
required/forbidden taxonomy prefixes check placement. Local atomscan also shows
only neutral documentation/disclosure findings for the moved rules.

The final soft run passed all 1,631 fixture checks, including the four controls
at their cap of 5. Local atomscan scores were 1 (placeholder), 2 (removal),
4 (CTF), and 3 (factfinder); only CTF produced the disclosure finding. All moved
documentation findings were notable. The four-tier scan found zero mixed rule
directories, and all ten effective-definition mappings verified. Strict
validation reports 176 oversized directories and the six platform-scope
findings described above, with no duplicate diagnostic. The overall migration
remains incomplete.
