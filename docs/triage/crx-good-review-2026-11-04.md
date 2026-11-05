# Chrome extension endpoint review — 2026-11-04

Review in progress. Initial scans covered 17 packages under 1 MB; package
permissions alone do not determine whether an extension is hostile.

`0b0f07942706` injects a script into an active WhatsApp Web page, extracts and
decrypts session key material from local storage and IndexedDB, and posts the
credentials to a third-party CRM. Its UI directs the user through connection and
explicitly discloses session extraction. The extension was initially recorded
bad, but this was corrected to **inconclusive**: the remote service's handling
and retention of the exported reusable credentials cannot be established from
the extension. The code establishes a sensitive transfer, not theft. Two broad
hostile composites were changed to suspicious extraction/upload clues because
co-occurrence does not establish unauthorized use; no artifact-wide exception
was added. The fresh scan has four warnings and no hostile findings. Validation
passed; Hopper and the hash-verified snapshot were corrected.

`bfb14e64a604` provides an externally callable cookie route to designated web
origins. It returns complete cookies for caller-supplied URLs and explicitly
recognizes session tokens for multiple services. The local extension shows
credential sharing, but not how the remote sites use or protect those cookies;
that unresolved external behavior makes the ruling **inconclusive**. Two new
suspicious findings describe the cookie route and external handoff; removing
the external listener prevents both matches. Validation passed, Hopper recorded
the label, and the snapshot was hash-verified.

`d56eb1a4d2c7` is a browser automation agent. Its content script accepts
messages from any same-origin page and forwards tool calls; the background
worker has a tool that reads cookies for a caller-supplied URL and returns
up to 30 characters of each value. This is a serious exposure to visited web
pages even though the agent's documented purpose is browser automation. A new
archive-level suspicious trait binds the page bridge to the cookie-reading
tool; a control with the bridge disabled does not match. The artifact is good
with this warning, not a proven malicious implant. Validation passed and Hopper
confirmed the label.

`9eccf8f01107` numbers Google search results and sends a user-entered license
key for validation; `56784473f92e` displays the rendered font; and
`42948a6e5ac4` adds download controls to VK audio. Their scripts and external
requests were inspected, fresh scans show no severe findings, validation
passed, and Hopper confirmed good. The pending VK snapshot was hash-verified
and moved to the good pool.

`1f3c07ccfa44` is a HiWorks login and attendance helper. It stores the
user-entered login password directly in extension local storage for later
login, and can send configured Telegram notifications. One new suspicious
trait reports the unencrypted password storage; a control without the write
does not match. No credential transfer to the notification service was
established. Validation passed and Hopper confirmed good with that warning;
the pending snapshot was hash-verified and moved to the good pool.

`8533c7ef5afc` is an image-only browser theme with no executable scripts.
Its fresh scan is clean; validation passed and Hopper confirmed good.

`d02e6c4d1eb5` adds VK audio-download controls and retrieves settings from
its service; `eb373c0314c0` integrates a CAPTCHA-solving service; and
`0dc1939587d8` provides AI-assisted social-post drafting through its configured
service. Their relevant scripts and network destinations were reviewed; fresh
scans show no severe traits, validation passed, and Hopper confirmed good.

`d781f61a468c` enhances SensCritique. It looks for an authentication token in
page state, storage, and cookies and uses the selected value in a GraphQL
request; the inspected caller supplies the SensCritique GraphQL endpoint. An
existing hostile rule incorrectly inferred exfiltration from a storage sweep
near an HTTP request. Two similarly broad proximity rules were relocated as
suspicious observations without whole-file or test-directory exceptions. The
fresh scan gives this extension one warning, validation passed, and Hopper
confirmed good; the pending snapshot was hash-verified.

`57ea5b283d74` and `66b891657517` are packaged browser games; the former
opens its publisher's game page on installation, and the latter includes an
unused template for a version/launch message handler. `f3a4a1e10d23` is an RSS
reader. The manifests and relevant scripts were reviewed, fresh scans show no
severe findings, validation passed, and Hopper confirmed good.

`1d2297ccbdbb` integrates Internet Download Manager with a native companion.
It collects cookies for download URLs and supplies them to the companion; one
new warning describes that sensitive handoff. Removing the native connection
from a control prevents the match. The fresh scan and validation passed, Hopper
confirmed good, and the incoming snapshot was hash-verified and moved.

`8ac7cbea819f` is an SEO inspector: it reads metadata from the active page and
submits the page URL to Google's PageSpeed API. The fresh scan has no severe
findings; validation passed and Hopper confirmed good.

`93bb1ea848c4` is AdGuard Extra. Its userscript modifies page and network
behavior for site-specific ad blocking; no credential collection or downloaded
code execution was found in the reviewed script. The fresh scan is clean,
validation passed, and Hopper confirmed good; the pending snapshot was
hash-verified and moved.

`8196c0c5f42c` is a cryptocurrency wallet. Its reviewed network calls query
balances, transactions, indexer data, prices, and submit signed transactions;
no private key or seed upload was found in those calls. The fresh scan has no
severe findings, validation passed, and Hopper confirmed good.

`7d25bcb21c8b` is a bookmark manager with history, search suggestions, and
optional backup functionality. Its relevant data handling and external search
requests were reviewed; the fresh scan has no severe findings. Validation
passed, Hopper confirmed good, and the pending snapshot was hash-verified.

`60d7de3d79a4` provides video meetings and co-browsing. When co-browsing is
requested, it installs a session rule that sets `Access-Control-Allow-Origin:
*` for stylesheet responses globally, before the desktop-capture picker. This
is security-relevant even though the co-browsing feature is disclosed. One new
warning describes the relaxed stylesheet CORS rule; removing the header from a
control prevents the match. Validation passed and Hopper confirmed good; the
pending snapshot was hash-verified and moved.

`b88677655b3f` adds HTML editing to Gmail and integrates with CloudHQ. Its
manifest, messaging, and relevant network calls were examined; no credential
collection or covert upload was established. The fresh scan has no severe
findings, validation passed, and Hopper confirmed good; the pending snapshot
was hash-verified and moved.

`7296b2b69e76` is a subtitle and language-learning extension with optional
local Anki integration. Its manifest and relevant network and browser access
were reviewed; the fresh scan has no severe findings. Validation passed, Hopper
confirmed good, and the pending snapshot was hash-verified.

`0b1531a587c6`, `67f0608cc7d8`, and `86dc1e810d33` are new-tab wallpaper
extensions. Their reviewed search code uses Chrome's search API. They open
publisher promotional pages on install and configure uninstall pages; the
first two use campaign tracking and the third has a potentially unwanted
promotion warning. Each fresh scan has one justified suspicious finding and no
hostile findings. Validation passed and Hopper confirmed the good labels.

`1d2ae767fa14` tracks job applications through configured JobSnap services;
`90b2bb26bc5d` integrates freight quotations with Gmail and uses an
interactive OAuth flow with its configured backend. Their message and network
flows were reviewed; fresh scans have no severe findings. Validation passed,
Hopper confirmed good, and pending snapshots were hash-verified.

`5a905899dfee` is a translation extension using configured translation and AI
services; `9ead77e2e8fe` organizes and imports sources into NotebookLM. Their
permissions, relevant scripts, and service destinations were reviewed. Fresh
scans have no severe findings; validation passed, Hopper confirmed good, and
pending snapshots were hash-verified.

`5823d9b1d2c9` is a Temu seller assistant that intercepts requests carrying
an `anti-content` header and collects cookies for the request URL. When its
login-state message sets `isLogin` and the collected cookie, anti-content,
user ID, and device fields are present, it posts those values to a separate
service. A duplicated timing check prevents the listener's immediate upload
when `isLogin` is false; the login-message path can still trigger the POST.
This is automatic session-credential collection and third-party transfer, not
merely a documented manual session migration. Two new hostile traits describe
the collection and POST; removing the dispatch in a control prevents both
matches. The fresh scan and validation passed, Hopper recorded bad, and the
snapshot was hash-verified.

`e7478cf40d61` checks WhatsApp number registration and integrates with the
WADesk service. Its optional cookie listener concerns the WADesk identity
cookie; the reviewed code does not extract WhatsApp session keys. The fresh
scan has no severe findings; validation passed, Hopper confirmed good, and the
pending snapshot was hash-verified.

`a0a2226ffe05` is a dropshipping helper. Its content script accepts
page-supplied bridge messages with the extension's app ID and matching tab ID,
forwards background function calls, and the background dispatcher includes a
function that can read cookies for caller-supplied parameters. This exposes a
sensitive trust boundary; the package does not establish malicious intent or an
actual theft. One new archive-level warning binds those two code paths; a
control without the cookie function does not match. Validation passed and
Hopper confirmed good with the warning; the pending snapshot was hash-verified.

`144b7d848ae0` and `3e88abc35cc7` are versions of a microphone noise
cancellation extension. They replace the browser media acquisition function
and initialize a local audio model with a remote SDK authentication exchange.
The reviewed initialization obtains its auth payload from model configuration;
no claim is made about unexamined service-side handling. The newer version can
send a promotional Google Meet chat message only after an in-product consent;
one of that behavior was found in the older version. A new warning explicitly
says the message is consented, and a control without the send action does not
match. Fresh scans report one warning for the newer version and none for the
older, validation passed, and Hopper confirmed both good.

`35c69076a932` captures tab audio for user-requested noise filtering and uses
the same model SDK; its fresh scan is clean. `f12d416a5199` applies webcam
effects and records video. On every tab activation it calls
`chrome.browsingData.remove` without an origin filter to clear service workers,
which earns one warning; it also includes the active tab URL in feature
telemetry. Removing the clear call from a control prevents the warning. The
fresh scans and a full validation after those rule changes passed; Hopper
confirmed good, and the pending audio extension was hash-verified.

`461f529ca076` is a tab manager that extracts unique words from page bodies
and stores them locally to search discarded tabs. One new warning describes
this page-content indexing; removing the response in a control prevents the
match. `f037b4eff72d` is an AI bookmark assistant that can submit page text and
bookmark-folder paths to a configured AI service. One new warning describes
that data flow, and a control without the network call does not match. Fresh
scans and validation passed, and Hopper confirmed both good labels.

`e32f897101ec` is a property-listing insights extension. Its content script,
OAuth flow, and service endpoints were reviewed; the fresh scan has no severe
findings. Validation passed, Hopper confirmed good, and the pending snapshot
was hash-verified.

Chrome-extension total: 37 good, 1 bad, 2 inconclusive.
