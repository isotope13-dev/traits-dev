Evidence and detection review: feed article 4367

Sources
https://thehackernews.com/2026/10/hackers-infect-953-online-stores-with.html
https://sansec.io/research/magento-cms-block-loader-deepveindrilling
https://sansec.io/research/polyshell-mass-attack-wave
https://github.com/0x4D31/honeypot-data/blob/main/reports/php2shell/2026-10-24-confirmed-rce.md

The supplied article.txt ends mid-sentence. Recovered article.html and the
linked primary reports are saved in the article scratch directory, along with
extracted text, code blocks and images. The THN m-code.jpg is an illustrative
image, not a specimen; its illustrative /loader.js URL and eval code were not
used to reconstruct malware. Sansec's timeline image contains campaign dates
and domains, not executable code. The Sansec reports publish actual loader
code in pre blocks, including the entire March loader and October replay stub.

Artifact retrieval
Forager was tried against https://deepveindrilling.com/?s=d35c5031 (HTTP 200,
empty body on all attempts) and https://lanhd6549tdhse.top/KZtBscgb (HTTP 522
on all attempts). No original endpoint bytes were recovered. Consequently
there are no successful Forager downloads or .forage.json files to relocate.
The HTML code blocks copied from Sansec are preserved in scratch/extracted/.
Their executable inline script contents were extracted, without HTML tags,
into the suspicious sample tier. These are published-code reconstructions,
not retrieved original endpoint payloads. The October script's external src
is recorded below; its response bytes are unknown and are not synthesized.

Samples
suspicious/october-cms-loader.js: exact inline October replay stub, reads
fpCode, installs that code into a new div's onclick handler, appends/clicks/
removes the div. The cited second script URL is
https://deepveindrilling.com/?s=d35c5031 .
suspicious/march-cms-loader.js: complete inline March code from the primary
report. Reads 136c1e07507f4a97, Base64-decodes the stored code into an anchor's
onclick handler, clicks it, deletes the storage entry, then loads the encoded
remote script with referrer, title and URL-query parameters.
suspicious/renamed-loader.ts: representative TypeScript form of the October
technique with renamed variables/key/tag, window.localStorage and a typed
HTMLElement. It adds no behavior beyond the cited source.
suspicious/decoded-renamed-loader.js: representative renamed March replay
stage with globalThis.localStorage, const declarations and atob decoding.

Scope and taxonomy
synthetic-click-code-evaluation is suspicious eval concealment: the same
newly created element receives dynamic onclick source and is clicked directly
or immediately after appendChild. It has no dependency on a campaign hostname,
Magento marker, storage key, attacker filename or collector-assigned name.
web-storage-event-code-replay is suspicious staged source activation: it binds
the getItem result, its guard, the raw or atob-decoded handler argument, and the
created/compiled/clicked element. It requires actual source-to-sink structure,
not a storage API somewhere in a file with an unrelated click handler. Both
rules use syntax queries for JavaScript and TypeScript on Unix and Windows;
no English prose matching or unsupported operating-system marker is used.

Removed dist-tail-injects-encoded-remote-script from its legacy objective home:
its two required facts were merely a decoded script src assignment and a nearby
encoded HTTP URL. Neither proved a distribution bundle, appended tail, hostile
payload or unauthorized tampering. The ordinary encoded-loader control exposed
this unsupported hostile classification. The existing notable trait
micro-behaviors/process/create/load/script::dynamic-script-src-decode-assign
retains the loading observation; creating a second neutral copy would duplicate
it. The removed exact ID and ancestor selectors have no rule consumers. Its
removal is an intentional severity/claim correction, not a placement-only move.

All firing suspicious/hostile findings were reviewed against sample source.
After the correction the four samples each have exactly two suspicious traits
and no hostile traits. Cached-code execution and synthetic event evaluation
are distinct supported observations. A third hostile rule would require
unpublished payload behavior or an unjustified verdict for ordinary loading;
we do not add one simply to approach the 3-5-hostile goal.

Verification
CLEAVE_TRAITS_DIR=<checkout> atomscan --no-update --analyze local --mode slow
  --follow=none --format json <scratch>/testdata
All four samples meet the two-suspicious-or-hostile floor. Reports and the
floor summary are saved as final-atomscan.json and floor-check.txt in scratch.
The ML model's v18/v21 feature-spec warning is independent of trait firing.
Cleave facts were inspected for all four source samples, including the decoded
https://lanhd6549tdhse.top/KZtBscgb?&se_referrer= URL. Facts show anonymous
function flow-graph limitations, so rules use parsed syntax rather than
unavailable flow provenance in these IIFEs.

Ten controls are in cleave/tests/fixtures/browser-stored-code: preferences,
ordinary event listeners, literal handler code, unrelated receiver clicks,
comments/string examples, reassigned elements, ordinary encoded script loading,
cached handlers without a synthetic trigger, unrelated storage and shadowed
storage. The last two intentionally retain the generic synthetic-evaluation
observation but reject the cached-replay claim. All 14 positive/negative cases
passed testdata/browser-stored-code/verify.py. None executes the sample code.

Indicators
<scratch>/testdata/ENDPOINTS has 13 historically suspicious/malicious names
and IPs: five feed loader domains, hdfdsi84j3h.top and c85grt98sd.com from the
primary campaign report, leqdger.click and crypto-insider.top as observed
payload hosts, 162.35.99.94 from the article's separate PHP2Shell episode,
15.204.59.70 as the other confirmed exploit source in its linked report, and
104.28.208.84/144.48.4.242 as attempt-only sources, not confirmed RCE.
The first two .click loaders expired and were re-registered by a parking
operator; the old injected references remain historically suspicious. Clean
parking infrastructure abovedomains.com, researcher services, and victim/store
addresses are excluded. PTR names describing hosting registration are context,
not asserted as malicious destinations.

Additional exact campaign URLs are:
https://deepveindrilling.com/?s=49b7ca5f&fp=
https://additionalver.com/Mb2z8J
https://lanhd6549tdhse.top/KZtBscgb
https://neswnsssn.click/PKgJDPfF
https://manulfie.click/GKTD8cBz
https://hdfdsi84j3h.top/sFnnPFHm
https://c85grt98sd.com/1kYrdH
https://leqdger.click/ssl/
https://crypto-insider.top/ssl/
Other primary-report storage keys: fpCode, 136c1e07507f4a97, 136c1e07507f4a98.
Database content location: cms_block.content. Uploaded webshell location:
pub/media/custom_options/quote/ ; backdoor filename in linked March report:
accesson.php. These are contextual indicators, not required detection strings.

SHA256 contains 19 decoded multipart-body hashes supplied by the linked
PHP2Shell report (three preparation-stage bodies and sixteen execution-stage
bodies). They are request-body identities, not downloaded binary hashes, leak
cookie hashes or successful-execution guarantees. No MD5/SHA-1 were supplied.
The PoC Git revision d6f888ebd3f0e188bb662e16f23747afdf35e42f is a commit ID
and is excluded. Locally computed hashes of reconstructed/synthetic fixtures
are not promoted into the malicious-identity indicator file.
PURLS is empty: no malicious package coordinate or package version is asserted.
Magento and PHP versions describe victim software, not malicious packages.
CVE-2025-54236, CVE-2026-48356, CVE-2026-109618 and CVE-2026-109619 are
vulnerability context, not file/package identities. The honeypot report supports
the observed leak-guided CVE-2026-109618 chain, not a distinct -109619 path.

Coverage limits
The final payload and October 23 fingerprint-loader code were not published
or recovered. No traits assert payment theft, a wallet drainer, fingerprint
transmission, a particular exploit implementation, webshell internals or the
PHP2Shell second stage from prose alone. The main sample coverage is extracted
JavaScript/TypeScript. Cleave exposes no parsed JS AST for an HTML container,
so inline HTML/CMS blocks require script extraction for these syntax-bound
rules; no broad text co-occurrence rule is used to claim data flow in HTML.
