# Browser cookie callback POST review

Run `python3 testdata/taxonomy/extension-install-cookie-post/check.py` from the
repository root. `CLEAVE` can select the engine. Thirteen synthetic controls
exercise lifecycle acquisition separately from the source-to-send relationship.
The controls use reserved test domains and never make network requests.

## Sample review

Sample: Yarrowguard 3.5.3, SHA-256
`0894c1f791be4ed9516869b7bf647a821643cb90b94916e5bd9146b06cc3e8f4`.
Verdict: **MALICIOUS**, an attempted automatic browser-cookie export disguised
by the manifest's generic productivity description. This verdict does not
claim successful theft or successful installation of the distributed CRX.

All five ZIP members were compared byte-for-byte with the supplied extraction.
There is one executable source file: the 231-byte `background.js`. Its
`chrome.runtime.onInstalled` callback calls `chrome.cookies.getAll({})`,
serializes `cookies.slice(0, 2000)`, and passes that exact serialized value as
`fetch`'s POST body to a fixed HTTPS endpoint on port 8443. It ignores the
lifecycle reason, so both installation and update take this path. It provides
no user-controlled export interface or productivity functionality. There is
no obfuscation, payload loading, command execution, or local persistence code.
The license's apparent decoded string is incidental text, not executed code.

Second-review limitations matter: the manifest requests `cookies` but has no
host permissions or mechanism to acquire them. Chrome only returns cookies
for authorized hosts, so the packaged extension cannot enumerate arbitrary
website cookies with these declared permissions. See the primary
[Chrome cookies API documentation](https://developer.chrome.com/docs/extensions/reference/api/cookies).
The CRX2 header declares zero-length key and signature fields. The 60-byte icon
also has malformed PNG structure. Neither property proves malware or evasion.
No external malware feed or reputation claim was used for the verdict.

Cleave reported incomplete flow analysis for the anonymous callbacks; those
limitations were resolved for this review by tracing the complete source and
checking its actual argument relationships, not by trusting scanner scores.

The exact script was additionally evaluated with JavaScript for Automation
and stubbed lifecycle, cookie, and fetch APIs. No actual browser APIs or network
were used. Before the lifecycle callback there was no POST. Supplying 2,005
synthetic cookie objects caused 2,000 full records, including values and
HttpOnly flags, to be serialized unchanged. Supplying no cookies caused `[]`
to be sent. Both install and update reasons invoked the same operation.
This verifies the code's relationship and intended effect, not the manifest's
effective permissions or any live endpoint response.

## Trait changes and placement review

The old cookie convictions could join unrelated reads, JSON serialization,
URLs, and HTTP requests, including across files. The replacement AST queries
require executable syntax, lexical adjacency and matching identifiers. They
use no sample name, destination, exact size, or cookie-count constant.

| Old observation | Disposition |
| --- | --- |
| `objectives/exfiltration/http/browser-extension::extension-cookie-store-remote-exfil` | Retired; browser source takes precedence over HTTP transport. Replaced by the bound cookie-callback POST rule. |
| `objectives/supply-chain/hidden-payload/extensions/backdoor::extension-cookie-read-upload-handler` | Retired; co-occurrence neither proves upload nor package-inspection concealment. |
| `objectives/supply-chain/hidden-payload/extensions/backdoor::extension-cookie-api-exfil` | Retired; adding a manifest permission to co-occurrence establishes neither data flow nor a hidden payload. |
| `micro-behaviors/browser-extension/lifecycle::extension-external-url-literal` | Moved unchanged to `micro-behaviors/communications/http/url/domain`; URL presence is not a lifecycle operation. |
| `micro-behaviors/communications/http/cookies::chrome-cookies-get-all-unscoped` | Corrected description: empty filter requests accessible cookies, not every cookie in the profile. |
| `objectives/exfiltration/stealer/browser::js-browser-auth-state-obfuscated-exfil` | Consolidated away as redundant: every match already requires the hostile `js-browser-auth-state-http-exfil` plus a separately detectable decoder. Neither constituent changed. |

Resource-first placement puts automatic unfiltered cookie acquisition in
`credential-access/browser/extension` and a bound cookie-to-send chain in
`exfiltration/stealer/browser`. A second pass from the matchers' required
results reaches the same homes: the acquisition query requires no send; the
export query requires browser records in the HTTP body. HTTP transport and
package concealment are the nearest alternatives, but neither owns those
required results. Both new traits are suspicious: managed cookie backup or
migration can share these mechanics. Sample intent and trait criticality are
separate decisions; the incomplete manifest is not silently treated as a host
grant. The browser leaf remains at its 100-rule budget after consolidating the
redundant obfuscated-auth-state composite, rather than creating a count-driven
subdirectory.

No surviving rule references the retired exact IDs. The relocated URL
composite's two exact consumers (`tabs::bound-https-tab-opener` and
`extension-update-active-external-navigation`) now reference its new home.
Its matcher, scope, severity, exclusions, and type/platform defaults are
preserved. Ancestor selector audit found no lifecycle or HTTP URL/domain
selectors; the broad `browser-extension/` suppressor remains satisfied by the
namespace evidence already required by the moved rule. Broad exfiltration
consumers retain the source classification; removal from hidden-payload
selectors is intentional because no concealment was demonstrated. The retired
obfuscation-derived composite has no exact consumers; its required parent
still contributes the same hostile browser-exfiltration observation.

## Controls

The two positives cover the supplied sliced form and renamed variables with
`browser`, direct serialization, and an explicit `body` field. Near misses
cover unrelated POST data, another cookie variable, a non-body shorthand
property, reassignment, duplicate body/method fields, a domain-scoped read,
a user-click export, quoted API fragments, comments, and a different callback.
The user-click case retains only the cookie-export finding. The other
unfiltered lifecycle cases retain acquisition even when export is refuted.
These expected overlaps test each claim independently.

## Corpus expectation

The original walked-corpus fixture required at least one hostile finding,
which conflicted with the independently reviewed criticality. Its unchanged
bytes were moved from `hostile/supply-chain-corpus/crx/` to
`hostile/crx-yarrowguard-cookie-exfil-macos.crx`. An explicit malicious fixture
expectation now requires both exact suspicious traits and forbids hidden-payload
claims. The corpus was not globally relaxed, and the sample remains a malicious
regression fixture. Initial validation failed only on the old hostile floor.
