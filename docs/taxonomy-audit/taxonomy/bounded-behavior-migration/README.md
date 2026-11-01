# Bounded behavior migration

This batch relocates 273 rules and removes one unreferenced synthetic QNX
rule. It retires three legacy namespaces and reorganizes crowded destination
siblings. Match predicates, effective scope, confidence and severity are
preserved for every relocated rule. Descriptions clarify what the evidence
supports; a reference to an API does not become a claim of execution.

| Previous home | Destination | Analyst meaning |
|---|---|---|
| `micro-behaviors/data/db/sql` (70 rules) | `data/db/read/{records,column,key-value}`, `db/{query,open,config,write,schema}`, or the observed editor, protocol, import or diagnostic subject | Distinguish reading a particular resource, preparing a query, opening a connection and merely naming an interface. SQL syntax is not itself a behavior. |
| `micro-behaviors/data/db/read` (85 rules) | `read/{records,column,key-value}` | Preserve the object being read rather than collect every database read in one oversized leaf. |
| `micro-behaviors/process/create/spawn` (11 rules) | `create/{exec,hidden,subprocess/launch,shell/encoded}` | Child creation, concealed launch and encoded shell arguments have distinct interpretations. |
| Selected `process/create/exec` rules | `process/replace`, `create/start-process`, `create/subprocess/launch` | Replacing the current process image differs from creating a child. Keep structured subprocess and Start-Process operations with their existing siblings. |
| `process/create/subprocess` | `subprocess/{launch,capture,configure}` | Preparing a command, launching it and capturing its output are different operations. A bare bytecode prose description moved to diagnostic metadata. |
| `objectives/exfiltration/serialization` (12 relocated rules) | `objectives/exfiltration/stealer/credential`; `micro-behaviors/data/serialize/{schema-credential,envelope,binary}` | Credential collection plus outbound communication supports export intent. Credential-shaped fields, framing and serialization alone retain their specific preparation meaning. |

The unsupported `qnx-perl-exfil-beacon-call` rule matched a synthetic
`beacon('exfil'` spelling, had no consumers, and was removed rather than
assigned a real-world capability. Other QNX rules were not removed by this batch.

The exact source/destination mapping and original rules are in
[moves.json](moves.json). Counts in this table describe the original cohorts;
destination populations also include existing rules.

## Capacity and neighborhood review

The 33 destination directories range from 1 to 68 rules; see the calculated
physical and namespace populations in [destination-counts.json](destination-counts.json).

New and reorganized leaves stay below 80 rules. At 72, review the parent and
siblings and split by a durable behavioral or resource distinction. The
database read and subprocess splits were necessary to keep the destinations
away from that threshold. Both physical file locations and logical ID
namespaces count; filenames do not create separate budgets.

[check-layout.py](check-layout.py) prints both calculated populations for
every destination, fails at 72, and
checks the three retired namespaces. This is a batch headroom check, not a
claim that every existing directory is below 80. Existing larger leaves
remain migration work under the engine's temporary 93-rule gate.

## Reference behavior

Exact consumers were rewritten to the new IDs. Directory consumers were
reviewed for changes to the set of rules they select:

- [directory-consumers.json](directory-consumers.json) records the original
  affected references.
- [reference-repairs.json](reference-repairs.json) records 115 selector
  reviews and eight local alternative groups. Repeated reviews can occur
  within one rule.
- Where a directory changed its meaning, consumers enumerate the previous
  cohort under its new IDs. Existing `needs` thresholds remain intact.
- Eight consumers needed an explicit component group to retain an OR within
  an `all` requirement alongside an independent `any` threshold. Six use one
  shared evidence profile; two retain distinct local groups. These groups
  preserve boolean relationships rather than reintroduce legacy namespaces.
- Complete directory cohorts use directory notation. Partial selections
  remain explicit. [validation-repairs.json](validation-repairs.json) records
  the compression and helper consolidation after the initial reference pass.
  Ten alternatives outside their consumers’ declared file types were also
  removed; those alternatives could never satisfy the consumers.
- Additions to surviving ancestor references were reviewed by subject. This
  is not a proof that every preexisting broad consumer is ideally classified.

## Verification

Run from the repository root:

```sh
uv run docs/taxonomy-audit/taxonomy/bounded-behavior-migration/check-preservation.py
uv run docs/taxonomy-audit/taxonomy/bounded-behavior-migration/check-layout.py
CLEAVE_TRAITS_DIR="$PWD" atomscan --no-update --analyze local --format=json path --mode slow docs/taxonomy-audit/taxonomy/bounded-behavior-migration/cases > /tmp/bounded-cases.jsonl
python3 docs/taxonomy-audit/taxonomy/bounded-behavior-migration/check-cases.py /tmp/bounded-cases.jsonl
../cleave/target/release/cleave --traits-dir . test-rules docs/taxonomy-audit/taxonomy/bounded-behavior-migration/cases/start.ps1 --rules micro-behaviors/process/create/start-process::start-process-call
make validate
```

`make validate` passed: 13,920 fixtures (1,927 hostile, 1,774 suspicious,
8,883 notable and 1,336 baseline). The only additional engine message was an
informational notice about condition spellings scheduled for retirement.

The preservation check passed for all 273 relocated rules. The 45 static
positive and near-miss cases passed their raw-trait assertions. They cover
query targets, connection and schema evidence, process replacement versus
child creation, subprocess launch versus output capture, credential export
versus serialization, protocol framing, hidden launch and encoded arguments.
The fixture source is analyzed, never executed.

The scanner omits the simple `start-process-call` OR composite from its output;
the case therefore asserts its two underlying observations. A separate
`cleave test-rules` check confirmed the composite matches `cases/start.ps1`.
No matching rule was strengthened merely to force it into output.

Two engine admissions accompany the migration: allow `replace` as a direct
process subject and retarget the existing broad-text exception for Chromium
column-query observations to their new file. Neither increases a directory
budget or broadens the exception's population.

This batch does not complete the remaining dropper or other large legacy
migrations. The migration map in [TAXONOMY.md](../../../../TAXONOMY.md) tracks
those separately.
