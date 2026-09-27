# Telnet relay classification

This audit covers the Telnet rules in the former stdio leaf, their PTY siblings,
and an overlapping IoT shell file. The [six-entry ledger](telnet-relay-mapping.json)
records the effective original definitions and their dispositions.

## Classification and evidence

Telnet is a channel utility here; the required mechanism is a stream bridge.
Neither named-pipe creation nor a shell command establishes a pseudoterminal.
The new rules therefore live in `reverse-shell/stream-bridge/telnet.yaml`.
No new utility directory or parent-level rule is needed.

| Previous rule | Finding and disposition |
|---|---|
| `stdio::reverse-shell-telnet-fifo` | FIFO creation, interactive sh and an external Telnet endpoint can be unrelated. Replace with a query relating FIFO creation, both path uses and the shell/network pipeline. |
| `backdoor/shell/reverse::telnet-fifo-reverse-shell` | Same four required legs as the stdio rule, with different scope/exclusions. Consolidate into the same FIFO relay definition. |
| `pty::telnet-pipe` | The middle command could be sed, not a shell. Replace with a shell positioned between two Telnet channels. Preserve package-script coverage through a structured `scripts.*` value matcher. |
| `pty::mknod-telnet` | Two nearby command names prove neither FIFO creation nor shell transfer. Retire this weak aggregate; the new FIFO relation recognizes `mknod PATH p` as well as mkfifo. |
| `pty::telnet-comp` | An umbrella over the two flawed patterns. Retire; callers may use the canonical stream-bridge rules. No external exact-ID consumers were found. |
| `backdoor/shell/reverse::persistent-telnet-reverse-shell` | Four printed strings reproduce its hostile verdict. It requires no cron write, activation, tunnel connection or shell transfer. Retire while retaining the primitive observations. |

The source queries cover a FIFO read by cat into a shell/network pipeline, a
shell reading the FIFO directly, and the reversed network-to-shell orientation.
The created FIFO and both path uses must agree lexically. Input/output redirects
must use default standard descriptors; `2< fifo` and `2> fifo` cannot substitute
for stdin/stdout. A supported stderr-to-stdout redirection is checked explicitly
in the cat-pipeline form. The two-channel pattern requires a shell command in the
middle position, not an arbitrary filter or a nearby shell elsewhere.

Complete relational patterns are suspicious attack-context observations in the
same objective leaf. Hostile composites reference those patterns plus canonical
Telnet endpoint evidence. Package endpoint evidence is a neutral observation in
`micro-behaviors/communications/socket/telnet`; it reads declared scripts, not
arbitrary manifest descriptions. This respects the rule model's separation
between atomic observations and hostile composites without duplicating matchers.

## Reproductions and controls

A local shell with its own FIFO and an independent Telnet request scored **242**
with two hostile reverse-shell verdicts. It now scores **4** with neither.
A Telnet/sed/Telnet pipeline scored **34** as a reverse shell; it now scores **2**.
A script merely printing the service, tunnel, cron-path and IP terms scored
**123** with the persistent-shell verdict; it now scores **4**.

Nine fixture expectations were added: four benign controls (independent local
shell, ordinary filter, mismatched FIFO/descriptor paths, and printed inventory)
and five positive controls (cat/FIFO, direct FIFO input, reversed mknod cycle,
two connections, and a declared package script). Benign controls forbid both
reverse-shell hierarchies. Positive controls require stream-bridge and at least
one hostile finding. The local positive controls score **119–124**.

The migration leaves two C# rules in stdio. PTY has 29 rules, stream-bridge has
38, and the neutral Telnet leaf has 11. All are below 85 and remain leaf-only.
The ledger's destination definitions verify and no stale fully qualified moved
IDs remain.

Full soft validation passes **1,653/1,653** fixture checks, including the 24
existing reverse-shell corpus checks. Strict validation reports **176 oversized
directories** and one additional exception-member error from a separate live
edit: `credential-theft/registry::pypirc-reference-test-fixture-context` references
`testing/presence/harness::test-or-declaration-file`, which is component rather
than notable. That definition is preserved for its own audit. No mixed rule
directories were found. The broader C# and taxonomy/cap migrations remain open.

## Limits and validator follow-up

These are syntactic relations, not runtime alias or control-flow proofs. Exact
path-token equality does not resolve differently quoted equivalent paths or
intervening variable reassignment. The initial FIFO patterns require explicit
mkfifo/mknod creation and standard redirects; unusual flags, explicit `0<`/`1>`,
other shell options, alternate executable paths, and heavily transformed command
strings need further representative samples. Canonical endpoint evidence still
requires a numeric port. The package-script matcher supports the two-channel
form; it does not claim to parse every embedded shell language.

Removing the old external-IP requirement intentionally admits domain names and
reserved/private test endpoints when the actual relay relation is present.
Broad co-occurrence-only matches intentionally disappear. Existing positive
corpus checks guard represented coverage, not every unrepresented syntax form.

**Potential validator improvement:** the two original FIFO composites had the
same four required legs but differed in platform declarations and exclusions.
Exact-equivalence validation should not erase these differences. A separate
review warning could report identical positive-evidence bodies together with
scope/exclusion differences, so authors can assess overlap without automatically
merging non-equivalent rules. The catalog should not acquire a second home for
one mechanism merely because its safeguards differ.
