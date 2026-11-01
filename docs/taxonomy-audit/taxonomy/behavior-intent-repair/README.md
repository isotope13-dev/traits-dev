# Restore behavioral meaning lost in migration

This batch repairs the four examples identified in the preceding audit and
their immediate siblings: 20 rules, with no severity or predicate changes.
It is not a completed audit of all legacy migrations or file profiles.

| Previous home | Repaired home | Meaning retained; limit |
|---|---|---|
| `metadata/file/profile/operation-cooccurrence` — VS Code search, FormData, sensitive-file clues | `objectives/credential-access/files/theft` | Likely credential collection and upload preparation; neither LLM use nor completed transfer is required. |
| Same profile leaf — service listing, stop/disable, miner or rival clues | `objectives/impact/degrade/services` | Service-disruption evidence; no bound victim service, rival-miner removal, or Kinsing identity claim. |
| Same profile leaf — cleanup message and unit operations | `micro-behaviors/os/service/config` | Service cleanup/configuration indicators; no required stop or deletion. |
| Same profile leaf — install hook and calculator launch | `objectives/supply-chain/install-hook/proof-of-concept` | Install-time execution proof-of-concept indicators; launch is not bound to the hook. The stronger Python rule stays distinct. |
| Same profile leaf — Insomnia plugin entrypoint and calculator launch | `objectives/execution/trigger/ide` | Plugin execution proof-of-concept indicators; archive scope does not prove import-time execution. |
| `metadata/lang/source/syntax/argument` — calculator launch clues | `micro-behaviors/process/create/exec` | Process-execution subject, without asserting that matched text executes. |
| `metadata/lang/source/syntax/assignment/member` — crypto exports, plus nearby import/export profile | `metadata/lang/source/interface/crypto` | Declared cryptographic interface, without asserting implementation, invocation, or library identity. |
| `metadata/file/profile/cryptography` — exports, import, and crypto API evidence | `micro-behaviors/crypto/provider/library` | Crypto capability, without asserting an export-to-call data flow. |

The API surface is a declaration, so it stays in metadata. Generic exports stay
in syntax. The former `exports-keygen-interface` alternates between scrypt,
randomBytes and createDecipher; its new name is `exports-crypto-utilities-interface`
because key generation is not required by every alternative.

`moves.json` records every original rule, inherited defaults, destination and
direct consumer edit. `check-preservation.py` compares effective predicates
after canonicalizing renamed references, including scope, severity, confidence,
file types, platform and size restrictions. Descriptions and IDs may change.

## Directory consumers

`directory-consumers.json` inventories all 45 affected directory-selector
occurrences. All are positive conditions; none is an exclusion or downgrade.
No live directory selector loses members in this batch. New membership reflects
the restored subject; this is not a promise that every downstream composite
has identical coverage after a taxonomy change.

The three consumers with `needs > 1` were checked separately. Two are PE-only
crypto/payload composites, while the relocated crypto composite is JS/TS-only
and already requires a crypto capability. The GitHub mailbox composite retains
its separate endpoint, write, authorization, client and loop requirements;
calculator command indicators enter its existing process-creation alternative,
not a new command-and-control identity rule. Its broad directory counting remains
an existing limitation, not a newly introduced threshold or role.

Other selectors retain their distinct context requirements. Service cleanup
remains configuration evidence; it cannot by itself establish startup
persistence. Credential collection/preparation stays distinct from the transfer
requirements of its exfiltration consumers. No compatibility aliases or broad
suppression rules were added.

All eight destination leaves remain below the documented 93-rule budget
(11–87 rules each); see `destination-counts.json`. The cap was not changed.

## Verification

From the repository root:

```sh
uv run docs/taxonomy-audit/taxonomy/behavior-intent-repair/check-preservation.py
CLEAVE_TRAITS_DIR="$PWD" atomscan --no-update --analyze local --format=json path --mode slow docs/taxonomy-audit/taxonomy/behavior-intent-repair/cases > /tmp/behavior-intent-scan.jsonl
python3 docs/taxonomy-audit/taxonomy/behavior-intent-repair/check-cases.py /tmp/behavior-intent-scan.jsonl
make validate
```

`make validate` passes: 1,927 hostile, 1,774 suspicious, 8,883 notable and
1,336 baseline fixtures (13,920 total). The existing deprecated-condition
spelling note remains; see `validation.txt`.

The preservation check and all 18 cases pass; every relocated rule has a
positive case. The scanner reports an older ML feature spec (v18 versus v21);
these checks assert raw trait findings, not model scores.

Cases are static synthetic evidence, never executed. Positive/near-miss pairs
cover credential search with/without multipart assembly; service disruption
with/without mining context; service configuration with/without the cleanup
diagnostic; install hook with/without calculator launch; calculator launch
without a hook; crypto declarations versus generic exports and crypto API use;
and plugin entrypoint with/without calculator launch.

The cleanup diagnostic's existing `.text` restriction requires an ELF section
for its positive case; the corresponding shell fixture records that the same
text outside such a section does not qualify. This batch preserves that scope.
The credential fixture uses `execSync`, which the existing child-process
composite recognizes; arbitrary imported `exec` aliases are not covered by
that composite. Neither limitation was silently changed during relocation.

## Merge prerequisite

Existing conflicts were reconciled before loading rules. Distinct CMOS matchers
retain distinct IDs; merged references use the surviving names. The empty
deleted Telegram stub stays deleted. Two deleted signature-claim atoms were
restored because their surviving Codex consumer still references them; no
artificial size filter was added to these parsed signature facts. The clipboard
cluster retains notable severity and its narrower API-reference description.
