# Browser sources and HTTP request capabilities

The [migration manifest](browser-source-moves.csv) records 55 moves. Browser
export falls from 106 rules to **78**; general request clients fall from 96 to
**85**. Both cap violations are resolved without an exception or a deeper split.
The duplicated `micro-behaviors/communications/http/body` branch is retired.
Placement contracts and tie-breaks are in [TAXONOMY.md](../../TAXONOMY.md).

| Subject | Placement and decisive evidence |
|---|---|
| Browser-owned credentials, cookies, state or browsing records with export | `stealer/browser`; the browser is the acquired source, not merely the implementation environment. |
| Browser OR wallet/cloud/mail-client credentials with export | `stealer/credential`; all alternatives concern authentication material, but no narrower store is required. |
| Browser/credential data AND screenshot, keyboard or clipboard collection with export | `stealer/multi-source`; the independent source classes must each be required. |
| Protected Storage password report with export | `stealer/keychain`; the OS-managed store is required, while browser ownership is not. |
| Credential acquisition without required transfer | `credential-access`; a helper does not inherit an export claim from its consumer. |
| Cookie access, analytics labels or JSON construction | The corresponding capability; none independently establishes theft. |
| Explicit HTTP exfiltration-header vocabulary | `exfiltration/http/header`; browser source and DNS context are optional in the audited composite. Ordinary headers remain neutral. |
| HTTP client mechanisms | `request/client`; use the more specific JSON, body, verb, authorization or configuration facet when required. |

Six source-alternative exports move to credential, six independent-source
chains to multi-source, and one Protected Storage export to keychain. The
browser/wallet acquisition helper moves to credential-access. Cookie and request
observations, analytics vocabulary, serialization, and an obfuscated workflow
leave browser export. Sixteen specific request facets leave the general client
leaf, which receives four label-adjacent request observations and the misplaced
cloud upload helper. Nine rules retire the duplicate HTTP body branch.

## A control exposed a real classification defect

`cloud-credential-upload-channel` was an OR over HTTP POST, upload, curl, and a
POST method. It required neither cloud data nor credentials. Because it lived
under stealer, a broad Discord rule accepted an ordinary JSON POST as theft
corroboration. It is now the neutral `request/client::http-post-upload-or-curl`.
The cloud-config stealer keeps its exact reference and its separate credential
read and path requirements. No matching condition or severity was weakened.

The new static controls distinguish an analytics label, ordinary analytics JSON
POST, and cookie export. All 12 assertions pass: the first two do not satisfy
the Discord theft classifier, while the cookie export still does. The fixtures
are scanned outside fixture-path suppressors and are never executed.

One existing benign corpus expectation named the old generic client directory.
It now requires the `request/json` category, supplied by the relocated
`http-post-json` observation, keeping
its score cap and forbidden environment-theft assertions. The POST-method atom
is suppressed by this fixture's test context; the JSON composite is the emitted
finding. This is an expectation-ID update, not a relaxed verdict.

## Distinct methods and loader repairs

The Go wallet file previously blocked validation: `count_min` over regex
alternatives counted occurrences, not distinct method names. The profile and
reporting groups now use separate atoms and `needs: 3`. Seven new atoms support
the groups; the wallet address extractor itself keeps its matcher and count.
Three inert Mach-O controls pass nine assertions, including repeated profile
and repeated reporting names. The [repair record](browser-method-repair.json)
contains original content, final definitions, and the intended coverage change.
Address extraction does not establish private-key theft or distinct providers.

Two concurrent edits introduced loader errors. The separate
[loader repair record](browser-source-loader-repairs.json) documents removing a
YAML filename from a reference and replacing unsupported URL-boundary lookahead
with a consuming boundary group. The latter retains the intended URL language
but includes a delimiter in the match span. These corrections are separate from
the 55 matcher-preserving moves.

## Remaining semantic work

Passing the cap does not certify all remaining browser classifiers. Next:

1. Reconcile the remaining recognized-cookie helper ORs. Named artifact identity,
   generic cookie utilities, and generic bundle shape do not share a theft home.
   Check direct and directory consumers before retiring redundant wrappers.
2. Review PyInstaller plus browser-cookie/request-module co-occurrence, unsigned
   HTTP clients with browser-or-Notes alternatives, Google mailbox reconnaissance,
   and native browser acquisition without a required transfer. These need precise
   source/tier decisions and controls, not a severity reduction to fit a directory.
3. Route the browser history/navigation exports still in activity/browser and
   tracking. Review their shared staging/payload ORs first: encryption OR storage
   does not necessarily establish staging, and serialization does not itself
   establish upload. Prefer semantic cleanup before creating browser subleaves.
4. Audit keychain siblings: some alternatives include non-keychain credentials,
   while some rules establish only local acquisition. A platform API alone does
   not make every associated credential browser-owned or keychain-owned.
5. Continue request sibling reconciliation. Exact body/JSON/verb facets now have
   documented homes; provider/library subdivisions and overly broad client ORs
   still require the broader implementation-layer audit.

Potential validator improvement: warn on an objective helper that is only an OR
of neutral capabilities and then supplies positive evidence to broad objective
directory consumers. Report the consumer path so the author can see the false
intent inference. This should be a review heuristic, not a prohibition on
composites inferring objectives from capability combinations. Existing validation
already rejects counted regex alternatives and checks duplicate matchers; this
pass found no identical atomic matcher-body overlaps among its moved rules.

## Preservation and final validation

Normalization checks preserve **377 moved/affected definitions** against the
118,812-rule migration baseline. The 55 moves change no effective matching
conditions, scope, confidence, criticality, thresholds, exclusions or mappings.
Sixteen descriptions and 14 local IDs were clarified. The separately documented
Go method repair intentionally refines distinctness and adds seven atoms.

The [directory-consumer report](browser-source-directory-consumers.csv) records
**92 affected references in 83 consumers**. Directory membership follows the new
subjects; exact references retain their semantics. Thirteen changes outside the
migration are reconciled in [the drift record](browser-source-concurrent-changes.json),
including the two separately identified loader corrections. They are not counted
as migration moves or silently overwritten.

The actual shared tree passes **1,841 verdict fixtures** with `validate --soft`;
no fixture or rule file is excluded. **73 focused assertions across 31 controls**
also pass: 38 existing stealer-source, 14 activity, 12 browser-source, and nine
Go method assertions. The final strict `make validate` remains failing with
**88 diagnostics**, including the broader cap backlog. Soft corpus success does
not mean strict policy validation passes.

The published snapshot measures **118,816 rules in 20,459 YAML files**, with
**149 oversized directories**, **16,746 rules in them**, and **4,081 excess rules**.
There are no cap exemptions; all receivers are strictly leaves within 85. No
rule directory exceeds depth five. Sparse review retains the 35-rule sibling
threshold. Atomic overlap review records 105 groups / 235 rules touching
violators and 433 groups globally. These are review candidates, not necessarily
mergeable equivalent definitions.

The cumulative disposition ledger contains **1,036 implemented entries out of
1,039**, with three sweep reviews. This ledger is not the complete semantic
backlog, and this checkpoint does not complete the taxonomy migration.
