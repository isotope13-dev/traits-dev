# HTTP capabilities, source inference, and remaining sweep rules

This pass resolves two cap violations by correcting existing category boundaries,
without adding subdirectories or exemptions. The [82-entry manifest](http-capability-moves.csv)
records **81 moved definitions** and **one inlined helper**. Eighty moved rules
retain their bodies and effective settings after reference normalization. Yarn
bundle identity retains its predicate and scope but changes from component to
notable, making the independent artifact identity visible. Fifteen names or
descriptions were clarified; the Python and Node collectors no longer claim
independently required source classes.

| Leaf | Before | After | Boundary correction |
|---|---:|---:|---|
| micro-behaviors/communications/http/upload | 94 | 66 | Headers, form preparation, suffixes, Blob construction, and package identity leave upload. |
| objectives/exfiltration/http/collect | 121 | 83 | Bare endpoint/configuration observations move to capabilities; identified stolen data follows its source. General HTTP collectors arrive from sweep. |
| objectives/exfiltration/http/upload | 177 | 176 | Raw `POST /exfil` path moves to endpoint evidence. This leaf remains over cap. |
| objectives/exfiltration/stealer/sweep | 13 | 4 | Source-defined exports, neutral helpers, and two general HTTP collectors receive their proper homes. |
| micro-behaviors/communications/http/header/custom | 81 | 85 | Named headers belong here even when an upload detector consumes them. |
| micro-behaviors/communications/http/form | 32 | 49 | Multipart fields/attachments and form submission share one existing home. |

The request/form/header contracts are documented in TAXONOMY.md. Pure form
preparation does not imply transmission; a gzip MIME label does not imply
compression; `/exfil` names an endpoint without establishing a source. An IP
upload-target composite admits bare IP and IP:port alternatives, so its common
subject is `ip/endpoint`, not exclusively HTTP URL syntax.

## Preservation and deliberate changes

Before each move batch, the complete catalog passed comparison after normalizing
references. A final comparison covers all **118,798 prior definitions** against
**118,797 current definitions**, allowing only the declared moves/renames, the
Yarn identity visibility change, and equivalent helper inlining. It compares
scope, conditions, exclusions, defaults, confidence, criticality, and mappings;
comments and descriptions are excluded from matcher identity.

The former Android transport helper was a disjunction of raw-body option,
endpoint, and header evidence. It had exactly one explicit consumer and exactly
the same document scope/settings. Inlining its alternatives converts
`source AND (option OR endpoint OR header)` into the consumer's `all: source`
plus `any: option, endpoint, header`. The consumer's match logic is unchanged.
The redundant helper is removed so its header alternative cannot supply an
independent upload-directory vote. Controls for source plus POST, source plus
header, and source without either retain their prior results. This does not
claim that headers prove transmission; the source-specific inference remains
explicit and independently reviewable.

Broad directory membership changes deliberately. Headers, script suffixes, Yarn
identity, and bare form fields no longer acquire upload or exfiltration meaning
through their old placement. Explicit consumers retain references to relocated
observations. A form-preparation control still matches the form and external-IP
observations but fails the upload-target composite; a file-upload call plus the
same endpoint matches it. Both controls assert the IP observation too, avoiding
a vacuous negative caused by an excluded or unrecognized address.

The Python profiled collector still counts observations across acquisition and
export predicates; it does not claim that its threshold counts independent
sources. The Node collector can use development/environment clues rather than
multiple secret datasets. Both now use the common HTTP collection behavior.
Their relocation does not establish the security precision of every alternative;
keep reviewing broad collectors against concrete controls.

## Duplicates and audit precision

Three identical atomic-body families were inspected: octet-stream headers,
JPEG headers, and `/exfil` path literals. Effective type/platform scope and/or
confidence differ, so this pass does not blindly merge them. The JPEG framework
helper and Lua/Outlook path observations remain candidates for neutral placement
and scope-aware consolidation. The two decoder collectors also share predicate
bodies but differ in package/file scope and applicable types.

The audit's matcher-overlap CSV covers **atomic if-body groups touching current
oversized directories**. Its count falls from 108 to **105 groups / 235 rules**
because two directories cease violating the cap, not because three duplicates
were eliminated. The new global metric reports **433 atomic overlap groups**.
This distinction is now explicit in summary.json.

The structural audit now agrees with the chosen guidance: depth **greater than
five** and multiple sibling branches with **fewer than 35 descendant rules** are
review signals. A single-child chain is not flagged by itself. Boundary checks
cover 34 versus 35 rules, a legitimate single-child chain, and depth six.
These remain organization heuristics, not automatic evidence of a bad taxonomy.

## Verification and remaining work

All **1,837 verdict fixtures** and **18 focused source-routing assertions** pass.
Strict validation retains **70 reported issues**; its only changed diagnostic
is **156 oversized directories**, down from 158. No new migration diagnostic
remains. Every receiving leaf is strictly leaf-only and within 85. The working
tree has **20,206 YAML files**, **118,797 rules**, and **4,329 excess rules**,
down by 46. Counts include unrelated working-tree changes and do not establish
downstream ML equivalence.

The [389-row provenance ledger](stealer-source-dispositions.csv) records **385
implemented** dispositions and **four reviews**, all remaining in sweep:

- `android-webview-location-file-spyware`: permission/WebView/Base64 evidence
  needs a concrete capability-versus-spyware counterexample before logic changes.
- `native-mcp-snapshot-upload-language`: protocol-unspecified snapshot/export
  wording needs a neutral data-transfer home; neither HTTP nor theft is required.
- `screencapture-with-creds`: local screenshot collection, not export. Reconcile
  its destination with the already oversized screenshot/capture leaf.
- `binary-exfil-to-ip`: headers and raw-IP context do not require an upload;
  review the transfer claim with a focused counterexample.

The now-under-cap HTTP leaves still contain broader semantic debt. Cap compliance
is not proof that every retained collector is precise. Continue with those four
rules, remaining surveillance sources, and the 156 catalog-wide cap violations.
