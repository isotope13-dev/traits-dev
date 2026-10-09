Second review of uncorroborated convictions
=========================================

ollama-swarm-relay-live.py — BENIGN

This is a Python Ollama inventory and inference-routing control, not a proven
cryptojacker. It declares 24 public IPv4 HTTP endpoints, concurrently requests
/api/tags, indexes returned model names by server, chooses the first matching
server, and POSTs the caller's model/messages to /v1/chat/completions. There is
no exploit, credential acquisition, authentication bypass, shell execution,
persistence, or evidence establishing lack of authorization. The comment
calling it a hostile positive control is not behavioral evidence. Public fleet
reconnaissance remains suspicious; inference and direct-IP HTTP stay notable.
Calls are defined rather than invoked by a module-level entrypoint. Cleave
reports flow-field-unavailable and flow-query-incomplete; source inspection
establishes the routing relationship, rather than inventing a flow fact.

pad26_128.com — MALICIOUS

A 26-byte DOS direct-action overwriter, followed by 102 zero padding bytes.
Rizin x86/16 disassembly at COM origin 0100h shows the initial '*.*\0' bytes
also execute as SUB CH,[002Ah]. AH=4Eh, DX=SI, INT 21h searches the wildcard;
AX=3D02h, DX=009Eh opens the default DTA result filename for update. XCHG AX,BX
preserves the returned handle; AH=40h, DX=SI, INT 21h overwrites that file at its
initial offset, then RET terminates via the normal COM startup stack. This tiny
form relies on conventional COM SI=0100h and inherited CX; copy length is not a
fixed specimen property. It does not iterate FindNext, preserve host code, or
check errors. No family attribution can be established from a wildcard alone.
The isolated MOV DX,SI write alternative now requires the preceding entry-mask
search sequence. A normal DTA-result data copy must not satisfy infection.

sweetalert2-11.17.2.tgz — MALICIOUS (contained browser sabotage)

The package is the SweetAlert2 dialog library and contains src/SweetAlert.js,
four readable dist bundles, and four minified bundles with the same live
routine. At module initialization it tests Russian navigator.language and
RU/SU/BY/Cyrillic-RF host suffixes. It records an initiation date in localStorage;
on a subsequent load more than three days later it disables document.body
pointer events, appends an audio element sourcing a remote Ukrainian anthem,
enables looping, and attempts playback. Autoplay can be rejected by the browser,
but the input-blocking side effect is independent. This is intentional regional
session sabotage, not an ordinary dialog option. No claim of credential theft,
installer execution, or compromise of the package publisher follows. The normal
new Function template parser is interpreter execution, not proven obfuscation.
JSDoc firstName/lastName examples are not account-member access.

Rule placement and consumer review
----------------------------------

* Public endpoint-count evidence moved from discovery to communications/ip/literal.
* GET/list co-occurrence moved to the same neutral leaf, renamed
  python-get-public-endpoint-list, and retains the existing HTTP-C2 exclusion.
* Removed the cryptojacking relay composite: discovery plus an unrelated /v1
  expression neither proves inference routing nor unauthorized resource use.
* Removed the C2 external-IP request composite in favor of the existing neutral
  direct-ip-http-client capability, including its payload-stager consumer.
* The Ollama /api/tags path moved from application identity to HTTP/LLM evidence;
  both exact consumers were updated. It does not identify the analyzed app.
* Worker-pool reference and ThreadPoolExecutor construction moved to work/pool;
  named consumers were updated. The generic create/workers ancestor used by a
  DDoS composite intentionally loses these pool-only observations: neither a
  pool reference nor executor construction alone proves worker creation.
  Remaining source-file rules retain their existing homes and matchers.
* The tiny wildcard/interrupt atom moved from Trivial-family identity to file
  search, retaining scope and size bounds; its family composite consumer now
  references the neutral observation. Other family rules are unchanged.
* firstName/lastName atoms now require actual structured member access and live
  in data/property/access. Their existing name-fields consumer was updated.
  Other legacy vocabulary predicates remain unchanged.
* The target-member rule describes container access without implying HTTP input.
* The browser-host description includes the optional Belarus suffix. The
  new-Function IIFE rule no longer maps ordinary evaluation to T1027/B0032.
* The DOS entry-mask overwrite composite requires image/extension-changing
  transfer evidence or the existing destructive-loop chain, not write setup.
  The latter preserves the Trivial.23 raw-byte fixture classified as C.
* Existing fixture expectations follow the renamed capability IDs; no verdict
  expectations were relaxed.

Verification
------------

All supplied SHA-256 values were verified. Each top-level sample was scanned
before and after editing, and cleave facts was collected for all three artifacts
and the four specified readable bundles. Sources were reviewed without executing
the samples. Rizin was used for DOS disassembly. Binwalk is not installed here.

Final expected counts (hostile, suspicious): Python (0,1); DOS (4,0);
SweetAlert2 archive and each sabotage-bearing source/bundle (2,0).
Hostile precision: DOS first-match 10.6, entry-mask 8.8, directory 7.8,
direct-action 7.8; regional sabotage 7.6; SweetAlert2 identity+sabotage 6.3.

cases.json records ten source positive/negative assertions plus DOS near misses.
Source assertions were checked against actual cleave reports. Both DOS fixtures
were additionally checked with explicit test-rules: unrelated buffer copies and
unbound SI writes fail self-image and infection rules; the data-copy fixture
still matches the neutral wildcard/interrupt observation. The neutral dialog
control has input blocking and looping audio but lacks regional gates and does
not match either hostile. The original samples supply positive controls for
fleet detection, the DOS image-write branch, and browser sabotage.
