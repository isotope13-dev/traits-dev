# Browser locations, access mechanisms, and collection evidence

The [95-rule manifest](browser-access-moves.csv) resolves two cap violations:
`browser/chromium` falls from **136 to 82**, and `browser/multi-target` from
**106 to 85**. All receivers remain strict leaves within 85. App-Bound Encryption
(**26**) and DevTools access (**6**) become mechanism-specific siblings beneath
browser; this adds no depth. The [contracts](../../TAXONOMY.md) distinguish them
from classic store access, generic APIs, neutral locations and collector output.

## Placement and sibling audit

Profile/history/configuration and mixed browser-store locators follow
`fs/path/application/browser` (**79**). Cookie-jar paths follow `fs/path/cookie`
(**22**); password/key-store references follow `fs/path/password-store` (**41**).
A pattern accepting Login Data OR Cookies is a browser-store locator; one
requiring Login Data is a password-store locator. This applies to Chromium,
Firefox and Safari evidence in source or binaries. None requires proof of
runtime activity, but a path does not establish a copy or completed read.

App-Bound key recovery and bypass take precedence over browser brand, DPAPI,
or injection details. DevTools cookie acquisition and enabling in-process
DevTools access follow that interface mechanism. Generic primitives keep their
existing neutral homes. Explicit collector/key-dump artifacts move to `loot`
(**47**), because an output marker does not identify its acquisition mechanism.
The new siblings are not proof that every retained classifier has sufficient
intent evidence; their remaining matcher questions are listed below.

Executable basenames follow `application/executable` (**73**); JSON string-field
fragments follow schema-object (**80**). KWallet/libsecret service, wallet and
schema references follow keyring (**9**). Cookie getter/setter method symbols
follow HTTP cookies (**80**). The sibling review leaves Firefox credential access
at **17** and Safari at **5**. Two different `key4.db` observations retain distinct
IDs: the bare filename and the browser-qualified reference. Their matchers differ
and were not merged merely because their old local IDs were identical.

The [label record](browser-access-labels.json) clarifies 27 descriptions;
five misleading IDs are also renamed. For example, a profile/store reference no
longer calls itself a copy, and JSON field syntax no longer calls itself loot.
The move-only overlap check found no identical atomic body touching a moved rule.
No confidence or criticality was lowered. One common ATT&CK value was hoisted to
file defaults after validation; effective settings are unchanged.

## Consumer changes and deliberate matcher repair

The [directory audit](browser-access-directory-consumers.csv) records **37 affected
references in 36 consumers**, including exclusions. Neutral locations no longer
supply acquisition evidence or suppress other theft evidence as a Safari collector.
Filesystem/browser-path consumers gain their actual locator subjects.

Six Chromium consumers explicitly retain the App-Bound, DevTools and four moved
collector-output alternatives. The JavaScript client classifier factors the
existing two defanged-IP alternatives into one neutral helper. The Python Telegram
classifier already requires the password SQL rule, making its Chromium-or-NSS
condition redundant; that tautological OR is removed without changing eligibility.
The [repair record](browser-access-consumer-repairs.json) stores before/after
conditions. **1,032 Boolean comparisons** verify the factoring and tautology
removal, excluding deliberate neutral-membership changes and the repair below.

Positive controls exposed two pre-existing dead defanged-IP patterns: YAML plain
scalars contained doubled regex escapes, and `is: external_ip` invokes a validator
that recognizes ordinary dotted addresses, not `[.]` or `(.)` notation. The two
patterns now recognize four valid 0–255 octets with no leading zeros. Public,
private and loopback addresses share this notation capability; the rules do not
assert routability. Invalid octets and leading-zero cases are rejected. This is
an explicit coverage repair, not claimed as matcher-preserving relocation.
Consumers supply their own behavioral context. A defanged address or a browser
path with an HTTP client alone does not satisfy the reviewed browser classifier.

The proof protects **205 original definitions**, allows only the recorded
consumer/matcher repairs, and separately verifies the new helper. The catalog
reconciles 118,816 before to **118,814 after**: one intentional helper addition
and the net effect of **15 outside changes** in the
[concurrent-change record](browser-access-concurrent-changes.json).

## Validation

Eleven focused controls pass **25 assertions**, covering location-only inputs,
DevTools acquisition with/without an HTTP client, App-Bound and output markers,
JSON fields without a collector, the ABE template, and valid/invalid defanged IPs.
The schema control is an inert PE built from retained C source because those
original rules are PE-scoped; testing the C source would not exercise them.
The established stealer suite adds **38 assertions** across 19 controls: **63
focused assertions** in total. Controls are scanned, never executed.

All **1,841 corpus fixtures** pass in a fresh temporary copy restoring only the
unrelated pre-existing shell-decoder rule described in the
[mail audit](MAIL-SOURCE-BOUNDARIES.md). No rule files or fixtures are excluded.
The [isolation record](browser-access-validation-isolation.json) contains both
shell definitions. The final five ID clarifications and default hoist preserve
effective matchers/settings; reference validation and the renamed PE control
were checked afterward.

Live soft validation still fails on the PyAigis shell-decoder regression. An
initial validation attempt also caught an unrelated decompression move halfway
through a concurrent edit; its temporary filename-bearing reference and mixed
leaf were gone on the subsequent run. Final strict validation reports **91
diagnostics**, including **147 oversized directories**. The audit does not
represent an isolated corpus result as a passing live-tree result.

## Remaining work and validator findings

- Finish the residual neutral-capability audit: browser SQL, key/decryption
  method names, encryption-field vocabulary and generic APIs still appear in
  credential-access. Do not classify every SQL query as theft, or discard a
  useful capability simply because it also appears in legitimate tools.
- Retire or refine the PyInstaller module-co-occurrence export and the ad-hoc
  signed browser-or-Notes/libcurl export. Neither requires a transfer; the latter
  has file-type-ineligible browser alternatives. Their exact IDs have no consumers,
  but broad stealer membership must be measured before retirement.
- Route the explicit extension-storage and silent-headless exports out of
  acquisition, and the Safari session-cookie TLS export by its source, after
  the 85-rule browser export receiver is reconciled. Do not add an exception.
- Review multi-target's wallet-only, persistence and generic module/name rules.
  Reaching 85 does not certify that remaining leaf's meaning. Likewise, ABE
  output/result labels plus an optional library or packaging clue need review;
  a protection-specific home does not establish hostile intent by itself.
- Validator improvements: warn when a format-specific validator cannot accept
  the matcher notation; flag likely doubled escapes in YAML plain/single-quoted
  regexes with a concrete counterexample; explain effective file-type-ineligible
  alternatives. These require semantic checks, not blanket string/style bans.
  Existing duplicate checks should still compare effective scope and exclusions,
  not merge merely equal local IDs or similar descriptions.

The ledger has **1,248 implemented dispositions out of 1,251**, with three sweep
reviews. The full taxonomy migration remains unfinished.
