NoMercy and WSO2 Carbon source-archive review

NoMercy.dll (SHA-256 df9b6668f20e2c3519f73d70e7af3b00322d49b2b10fafcaeabb71306806b436)
is MALICIOUS. This is a .NET 8 Windows credential/session stealer configured
by its builder to export to an embedded Discord webhook. Assembly metadata
calls it "Orion Utilities" and "Update helper". Local-export, help and
diagnostic modes are plausible utility features; the configured remote
credential export, concealed destination and enabled evasion tip the verdict.
No deployment or operator authorization context was supplied.

Static IL tracing, using dnfile/dncil, established these paths:

- `Program.Main`'s async state machine at RVA 0xff4c loads builder metadata,
  checks VM/debugger gates, applies evasion, scans browser stores and messaging
  sessions, writes reports, makes a ZIP and passes that path and the configured
  webhook to `DiscordUploader.UploadAsync`. Its upload state machines construct
  multipart content and call HttpClient.PostAsync. Temporary exports are cleaned
  up; KeepLocal is enabled in the embedded configuration.
- `RuntimeConfig.Unprotect`, RVA 0xab90, Base64-decodes WebhookBlob, then XORs
  each byte with nonce[i % nonce.Length]. This yields
  `https://discord.com/api/webhooks/[redacted]`. ZipLogs, AntiVm, AntiDebug and
  Evasion are all embedded as true. The destination secret is deliberately not
  included in this review or its fixtures.
- `BrowserScanner.ScanChromium`, RVA 0x4d94, discovers profiles, loads DPAPI
  keys and calls AppBoundKey.TryAcquire. RunHook (0x3e68) reads the APPB key,
  strips the prefix, writes a configuration/blob, copies abe_hook.dll to a
  temporary path and injects it into a browser using RemoteInjector.Inject
  (0xa5e0). The latter writes the DLL path into remote memory and starts
  LoadLibraryW through CreateRemoteThread. The hook sidecar is absent from the
  supplied artifact; successful key recovery was not observed or assumed.
- LoginExtractor.ReadProfile (0x9ad4) reads Chromium login rows and decrypts
  password blobs. ChromeCrypto.DecryptBytes (0x56c0) handles v10/v11/v20 with
  AesGcm.Decrypt. Cookies are also queried and exported.
- FirefoxExtractor.ReadLogins (0x8c68) stages key4.db/cert9.db/pkcs11.txt in a
  temporary profile. DecryptLogins (0x9180) reads logins.json and passes
  encryptedUsername/encryptedPassword to NssApi.Decrypt (0xf7f0), which calls
  PK11SDR_Decrypt through a delegate. These recovered records join the reports.
- TokenScanner.ScanDiscordDesktop (0xc928) enumerates LevelDB stores and
  recovers plain or protected tokens. Telegram desktop tdata and browser
  storage are collected into archives by CaptureDirectory (0xdc60). Reports
  and these captures enter the main ZIP upload.
- Evasion.HideThreadFromDebugger (0x82dc) resolves NtSetInformationThread and
  invokes it with pseudo-handle -2, information class 17, null and zero length.
  BlindEtw (0x8334) resolves EtwEventWrite, changes its protection, and uses
  Marshal.WriteByte to store 33 c0 c3 before restoring protection. Static paths
  establish intended effects; this review did not execute the specimen.

Both WSO2 archives are BENIGN: Carbon Kernel 4.9.0-m4 and 4.12.42, a Maven/Java
OSGi server framework and administration UI. Forager fetched the exact versioned
Go-module PURLs through proxy.golang.org and verified them with sum.golang.org.
Their bytes equal the supplied ZIPs, including SHA-256. Provenance records and
artifacts are retained in the task scratch directory, not reconstructed.
The upstream project is https://github.com/wso2/carbon-kernel; the archives'
Maven SCM declarations also refer to WSO2's carbon4-kernel repository.

The high-scoring EditArea 0.8.2 code is a syntax editor. Its gzip member expands
byte-for-byte to edit_area_full.js. Its eval paths dispatch configured editor
callbacks and frame methods; XHR loads a local template and scripts come from
the configured editor base. all.js combines Prototype and UI helpers: its
responseText/script evaluation implements the documented AJAX/script behavior.
jQuery, Prototype and YUI implement DOM updates, event handling, HTTP requests,
cookie helpers and legacy browser compatibility. These capabilities remain
detected. The admin index validates the authenticated session before requesting
server statistics; WSRequest implements caller-configured SOAP/HTTP operations.
CI runs Maven builds, and launcher/diagnostic code starts Java and queries host
status. The reviewed paths fit the distributed server framework, with no
evidence of injected credential theft or a backdoor. This verdict is not a
statement that old web libraries or every framework configuration are secure.

Trait corrections preserve matchers and effective scopes unless noted:

- Generic hostname helper calls move out of ICMP; Hazelcast onMessage
  declarations move out of WebSocket receive; fixed thread pools move from
  process creation to work pools; process input-stream access moves out of
  shell creation. Explicit consumers follow the moved IDs.
- jQuery UI's `this[this.isOpen?"close":"open"](t)` matched a rule whose only
  requirement was a Close string near an indexed call. The exact observation
  survives as source syntax, without an invented WSH/StdIn receiver.
- SyntaxHighlighter's copy-code button calls clipboardData.setData without a
  copy-event handler. Its description now states only the clipboard write.
- Three generic process-access-right names move out of daemontools malware
  identity and into process-handle rights. Their family composite keeps the
  same required conditions. HideThreadFromDebugger's name moves from hardware
  breakpoints to thread hiding, preserving its exact and directory consumers.
- The Chromium-only multipart export moves from multi-source to browser theft.
  The existing WinHTTP rule requires both browser loot and a host profile and
  moves in the opposite direction. Neither matcher nor severity changes.
- The class-17 CIL observation retains both old field-token encodings and adds
  the constructed pseudo-handle/native-delegate form actually present here.
  Its consumer remains a suspicious API/layout profile, not resolved IL flow.
- New rules cover the cyclic-key in-place XOR loop, managed AesGcm type
  reference, encrypted credential-field references and Firefox/NSS recovery.
  Generic encryptedPassword variable names in Java are not Firefox evidence:
  the field rules match exact names in managed PE/DLL artifacts.
- The new ETW profile requires export/protection/write names and the three
  CIL byte-write argument layouts in .text. It is suspicious because the
  matcher does not resolve the API pointer-to-write relationship. The actual
  program's ETW patch was established separately through IL tracing.

`review.json` records counts, classifier probabilities, renamed IDs, dependency
expansion and coverage comparisons. Raw scans, full facts, member facts, IL and
redacted decoded configuration are in scratch/fallout-pass. There is no lost
hostile or suspicious coverage in the batch or the independent attack controls.
The classifier's archive alerts remain false positives; legitimate code's
accurate capabilities were retained rather than suppressed to adjust scores.

Run the focused checks with:

```sh
python3 testdata/triage/nomercy-carbon-review/check.py \
  --sample /path/to/NoMercy.dll --scratch /path/to/disposable-controls
```

These checks statically scan a renamed positive, one-leg binary mutations and
ordinary Java/JavaScript controls. They never execute a DLL. Full before/after
scans additionally checked managed-smtp-credential-collector.exe,
greatnesscoming-managed-loader.dll, managed-native-interop-only.exe,
managed-status-stubs-only.exe and terminal-width-probe.java from this repository.
