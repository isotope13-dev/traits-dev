# Browser capability triage

Reviewed all three original samples with atomscan and cleave facts. Archive
members and the native PE were inspected independently. Cases in cases.json
were checked with cleave test-rules; every positive and near miss passed.

## Verdicts and corpus results

| Sample | Verdict | Hostile before/after | Suspicious before/after |
| --- | --- | --- | --- |
| @vyiiw/bundle 1.2610.607 | Benign | 0 / 0 | 1 / 1 |
| 355954d87688 Remcos native agent | Malicious | 4 / 4 | 8 / 8 |
| CyberStrikeAI 1.6.17 source archive | Benign | 0 / 0 | 1 / 0 |

Vyiiw is an obfuscated browser UI library. Its decoded runtime implements
windows, previews, docks and scrolling. Network operations retrieve icons and
same-origin license data; storage retains dock preferences. SHA-256 checks
license integrity. No covert collection or controller tasking was found.

Remcos installs WH_KEYBOARD_LL through SetWindowsHookExA, with an actual
keyboard callback and background logging threads. Its COM routine constructs
the CMSTPLUA elevation moniker and calls CoGetObject. The RC4-decrypted SETTINGS
resource contains controller endpoints, an installation filename, log path and
injection target. Process-memory writes and thread-context manipulation support
the existing hollowing detection. The elevation composite now requires COM
activation rather than only matching strings. Keyboard-hook/Winsock evidence
supports T1056.001; it does not establish HTTP transport.

CyberStrikeAI is an operator-controlled pentesting platform. Its CSRF skill
contains fenced form-submit examples. Its C2 templates use operator-supplied
server/token/key placeholders and are explicitly exposed by the product.
The documentation expression alone does not establish exploit execution.
No suspicious dependency finding was responsible for these three verdicts.
Final scans disabled reference following to confirm each artifact in isolation.

## Relocation and consumer audit

All exact live references were updated, including composite consumers and
exception references. Source directories retain their other rules. No broad
legacy-directory selector required widening to unrelated destination members.

| Old identifier | New identifier |
| --- | --- |
| execution/exploit/chain::html-form-autosubmit | ui/window/form-input::first-form-submit-expression |
| impact/cryptojacking/miner/signatures::coinhive-escaped-document-write | ui/window/dom-access::hex-escaped-document-token |
| process/create/load/remote-code::js-computed-document-member-call | ui/window/dom-access::computed-document-member-call |
| anti-static/obfuscation/encoding/arithmetic::repeated-hex-arithmetic-constants | data/arithmetic::repeated-hex-arithmetic-constants |
| anti-static/obfuscation/syntax::html-charcode-decode | data/string/conversion::charcodeat-text-expression |
| anti-static/obfuscation/syntax::html-fromcharcode-decode | data/string/conversion::fromcharcode-text-reference |
| anti-analysis/debugger-detect/browser::js-hex-constructor-token | data/property/access::hex-escaped-constructor-token |
| execution/interpreter/eval/dynamic::svg-hex-constructor-token | data/property/access::hex-escaped-constructor-token |
| anti-analysis/debugger-detect/browser::js-hex-debugger-suffix | process/debug/event::hex-escaped-debugger-keyword |
| anti-analysis/debugger-detect/browser::js-obfuscated-hex-debugger-antidebug | anti-static/obfuscation/string/dynamic::mangled-constructor-debugger-tokens |
| data/encoded::base64-token | data/codec::base64-helper-invocation |
| communications/dns/label::{common-source-dns-query-api,portable-source-dns-query-api,c-source-dns-query-call,source-dns-query-api} | Same identifiers under communications/dns/lookup |
| package/files/runtime::typescript-source-tree-artifact | package/files/runtime::source-tree-artifact |

Paths omit objectives/, micro-behaviors/ or metadata/ where unambiguous.
The unused partial debugger-prefix atom was retired. Full escaped constructor
and debugger words replace partial substrings; the SVG duplicate was merged
with the union of its previous scopes. The constructor/debugger composite
now describes token coexistence, not an inferred executed debugger trap.
Base64 invocation retains its matcher and exclusions, with Clojure, mIRC and
ircII removed from its broad scope to respect the destination filetype cap.
Other relocated matchers and scopes are preserved. Neutral complete operations
are notable: Base64 conversion, DNS resolution, socket operations, thread and
pipe creation, privilege lookup/adjustment and the WinInet API cluster.

Validation exposed dormant Go runtime CreatePipe names. The pipe atom now
requires an imported symbol, and its IPC attack attribution was removed.
