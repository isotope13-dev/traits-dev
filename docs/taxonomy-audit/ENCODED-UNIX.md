# Encoded shell carriers and independent commands

The [17-entry ledger](encoded-unix-mapping.json) records the removed verdicts,
relocated observations, effective definitions and reasons. This batch covers
Perl, Elixir and Kotlin under `reverse-shell/encoded`, plus the immediate
observations and proximity verdicts exposed by their controls.

## Findings and decisions

The Perl and Kotlin rules could convict a Base64-encoded `printf status-ready`
command without any network operation. Elixir joined an encoded local `bash -i`
command with an independent encoded HTTP health check into a reverse-shell
verdict. Decoding, execution and transport observations do not prove a relay,
even when they appear near each other.

All three actual corpus payloads already receive `reverse-shell/dev-tcp`
findings from their decoded content. The Perl rule's assertion that the engine
cannot recover this payload was stale. No replacement encoded-only mechanism
or language-specific objective is necessary. Four verdicts are retired;
positive fixtures now explicitly require the supported `dev-tcp` mechanism.
The existing Perl score and finding-count floors remain unchanged.

The new benign controls also exposed related placement errors:

- Elixir's variable shell-command argument is now a notable observation in
  `process/create/shell/command-string`; its command-dispatch consumer references
  the new ID. Predicate, scope and confidence are unchanged.
- Two decoded interactive-flag observations move to
  `process/create/shell/interactive` at notable, retaining their predicates,
  scopes, exclusions and confidence. Their existing execution-cluster consumer
  follows the canonical IDs. The redundant `any` roll-up is removed.
- The encoded shell-plus-transport conjunction is retired. Its two encoded-only
  pseudo-device path observations have no remaining consumers; the canonical
  neutral `socket/tcp::dev-tcp-path` still reports these decoded paths. Encoding
  does not establish an external endpoint's role or make a path malicious.
- Generic Base64 decode/exec and decode/subprocess proximity verdicts are
  retired. A PHP wrapper and a PyPI metadata wrapper added no missing payload
  relationship and are retired with them. Their decoder and execution atoms
  remain available. Two newly unreferenced suppressors are removed as well.

This deliberately removes unsupported intent claims, not just their criticality.
No fixture exemptions, rule-count exemptions or parent-level aliases were added.

## Verification

| Control or payload | Before score | After score | Result |
|---|---:|---:|---|
| Local encoded commands, Perl/Kotlin/Elixir archive | 271 | 4 | No reverse-shell or suspicious/hostile intent finding |
| Independent Elixir terminal and HTTP probe | 195 | 5 | No reverse-shell or suspicious/hostile intent finding |
| Perl encoded corpus payload | 238 | 128 | Two hostile findings; `dev-tcp` retained |
| Kotlin encoded corpus payload | 162 | 124 | Hostile `dev-tcp` retained |
| Elixir encoded corpus payload | 203 | 127 | Hostile `dev-tcp` retained |

Both new benign archives have score caps of 10 and forbid the entire reverse-shell
prefix. The validator also checks their members for intent findings. Required
neutral decoder and shell prefixes protect the useful observations.

The final soft run passes **1,665/1,665 fixtures**, including all 24 reverse-shell
checks. Strict `make validate` fails only on **176 oversized directories**.
The 17 ledger entries verify against effective current definitions and references;
no retired IDs remain in rule dependencies. The four-tier scan finds zero mixed
rule directories. Current leaf counts: encoded 3, interactive-shell 17,
command-string 10, encoding/content 45, payload/encoded 128. The last leaf still
needs its cap and semantic audit; these retirements do not finish that work.

## Remaining audit and validator candidates

The three surviving encoded rules are Python import/shell co-occurrence and PHP
packed shell labels. They still need mechanism-level evidence review. This batch
establishes coverage for the tested decoded carriers, not arbitrary encodings or
all forms previously admitted by the broad verdicts.

Duplicate-body validation cannot catch every duplicate observation. In particular,
`sh\s+-i` also matches the tail of `bash -i`, so the two flag matchers can satisfy
an execution cluster's `needs: 2` using one operation. Their exclusions differ,
so automatic merging is unsafe. Flag overlapping positive evidence for review,
and distinguish two rule IDs from two independent observations. The cluster and
the remaining encoded capability observations need a follow-up audit.

A second review candidate is an intent composite made solely from nearby neutral
capabilities: proximity does not prove data flow. Validation should surface the
missing relationship for review rather than treating a short distance, a package
container, or the names of the rules as proof of a malicious payload.
