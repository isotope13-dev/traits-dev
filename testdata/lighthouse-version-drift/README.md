Lighthouse 13.5.0-dev.20261016: BENIGN

Sample SHA-256:
84edea61773513924684275e62a1e17c4563d62a4b990d3ce437ca44ddd27f57

Fetched the immediately preceding published release from
https://registry.npmjs.org/lighthouse/-/lighthouse-13.5.0-dev.20261014.tgz
SHA-256: 9cec52e7172c5294b8dd8235f174c799a40c674cb5694e85afa4b52c8b11ab97.
Both archives match their npm registry SHA-1 and SHA-512 integrity records.
Compared every regular archive member: 985 files in each, no additions or
removals, 12 changed files. All three dist/report bundles are byte-identical.

Decisive diff evidence:
- scripts.zizmor is byte-identical in the two package.json files:
  uvx zizmor@1.25.2 --gh-token="$(gh auth token)" .github/workflows
- All script declarations and entrypoints are unchanged. There are no
  preinstall/install/postinstall hooks. Prepack builds reports and types;
  postpack cleans generated type files. Zizmor requires explicit invocation.
- package.json otherwise changes the version, removes lodash-es/ws and their
  types, and updates yargs/yargs-parser and their types.
- arbitrary-equality-map.js replaces lodash isEqual with a local recursive
  comparator for primitives, arrays, typed views, dates, regexes, maps, sets
  and object properties, with WeakMap cycle tracking. Four callers import
  this helper. swap-locale.js replaces lodash get/set with property traversal.
- baseline.js corrects a displayed feature date. insight-audit.js adjusts
  metric savings and numeric values. storage.js skips opaque null origins.
  Two declaration files follow implementation changes; another only reorders
  a union's types. No changed execution path collects or sends credentials.

The earlier release also fires the old token trait with the current pre-edit
rules. The historical queue's clean result is not reproduced by this rule
revision; the token command itself was not introduced by this release.

Behavior review:
cli/index.js calls begin() in cli/bin.js. core/index.js runs navigationGather
and Runner.audit; snapshot and timespan APIs use corresponding gatherers.
Chrome DevTools evaluation, page inspection and screenshots serve web auditing.
The manifest is the only location containing the gh auth token command.
It passes the user's existing GitHub session token as zizmor's API credential.
Zizmor documents precisely this usage and recommends it for local online
workflow audits: https://docs.zizmor.sh/usage/ . There is no token upload sink
or concealed install trigger here. Existing Sentry reporting is gated by
flags.enableErrorReporting and a 1% sampling decision; that code is unchanged.

Ran atomscan and cleave facts on the archive, plus facts on the manifest,
changed comparator and flow bundle. Inspected decoded strings using cleave
strings: the flow bundle's 330 numeric-radix renderings and one Unicode-escape
source slice are ordinary bundled report content. The axe valid-langs numeric
array is a trie of language codes: isValidLang follows letter indices through
nested arrays. It never decodes executable payloads. Source-analysis budgets
limit some flow queries; byte comparison and source tracing establish this
verdict independently of scan completeness.

Corrections:
- Replace the suspicious objectives/.../cli::gh-auth-token substring with
  notable micro-behaviors/os/security/auth/secret::npm-script-gh-auth-token,
  constrained to scripts[*]. Release/test script exclusions formerly hid
  other token queries anywhere in the same manifest; remove those exemptions.
  References in credential-harvest and webhook consumers use the new ID.
  Credential-access ancestor selectors inspected here have incompatible
  source types/file scope and do not need the package.json-only capability.
- Move long numeric runs to metadata/lang/source/shape and update the packer
  composite. Numeric arrays alone establish no obfuscation. Preserve matcher,
  type/platform scope and generated-parser exclusions; remove inherited T1027.
- Move the firing i18n/locale basename observations to metadata/file/naming;
  preserve scope/matchers and update the Unicode context composite. Drop the
  inherited Unicode-obfuscation MBC mapping from these name properties.
- Move permission wording atoms and their three OR groups to
  metadata/permission/prose. Preserve matchers, levels, scope and proximity
  consumers; remove the account-manipulation ATT&CK mapping from prose.
  Generic grant/must/permission words in Apache license text are document
  vocabulary, not account manipulation. Exact consumers are updated; no
  other references to those IDs exist. Removing these neutral observations
  from broad objective selectors intentionally removes unsupported evidence.
- Require the $ExecutionContext variable sigil, rather than a Chromium class
  name, and place the repeated embedded syntax under metadata/lang/source/syntax.
  Preserve the count/density/size gates and update the PowerShell consumer.
- Match parsed fullscreen calls in JS/TS, which excludes the deprecation
  message containing Element.requestFullscreen(). HTML currently lacks call
  records; keep its weaker text observation in a separate, explicitly named
  HTML syntax trait. The browser-lock consumer selects both alternatives.
- Bound the Sudvid vendor token so Danish tredjepartsudvidelser cannot identify
  the Quantomate product. No product-name allowlist or filename exemption.

Controls: python3 testdata/lighthouse-version-drift/check.py
All fixture programs are inert static-analysis inputs and must not be run.
They cover the token helper and description-only near miss; a manifest with
both release tooling and an install-hook query; fullscreen calls, message and
both together; Danish/vendor tokens; Chromium/PowerShell contexts; long/short
numeric runs; matching/nonmatching basenames; and grant prose. Low-tier prose
uses test-rules because unconsumed baseline findings are stripped from scans.
The webhook control asserts the token-query and curl observations. The
pre-existing webhook composite has an independent lifecycle suppression and
is outside these matcher changes; this control does not claim that composite
fires. This triage adds no new hostile claim.

Re-scan: atomscan completed with this worktree's traits. The independent JSON
report has 437 unique notable traits, zero suspicious and zero hostile; there
are no emitted objective IDs. All 19 focused controls pass.
Final validation command, after writing the judgement marker: make validate.
