# Expo Notifications, wp2shell and StormAttack first review

Verdicts concern the submitted bytes. No executable was launched as an OS
process, no exploit was sent to a target, and no malware endpoint was contacted.
`atomscan --no-update --mode slow --follow=none -f json` and `cleave facts`
were run on each original. Source/member facts, JADX, rizin disassembly and
PE resource inspection supplemented the archive-level facts. Fetching was
limited to upstream provenance and controls, not sample-controlled endpoints.

## Identities and verdicts

| SHA-256 prefix | Identity | Verdict | Deciding evidence |
| --- | --- | --- | --- |
| `9f4e0c35ea12` | Expo Notifications 57.0.24 | BENIGN | Registry tarball is byte-identical; traced code implements notification registration, scheduling and presentation. |
| `0d83a33117cd` | Crypto-Cat wp2shell 3.0.0, revision `e7220d170f9e` | BENIGN | Python source is byte-identical to upstream; transparent security-assessment CLI requires an explicit target and command. Dangerous functions are its disclosed purpose. |
| `87887525167d` | StormAttack resource DLL installer/injector | MALICIOUS | Traced self-copy/patch, Active Setup registration, service-DLL hijack, remote DLL injection and self-delete code. |

Expo's `getExpoPushTokenAsync` obtains the native push token, installation ID,
app ID and project ID, then POSTs this routing information to
`https://exp.host/--/api/v2/push/getExpoPushToken`. Its successful default
registration enables future updates. The import-time listener checks persisted
`isEnabled` before sending token updates and backs off/retries abortably. Web
push checks notification permission, registers the configured service worker,
and sends it notification icon configuration. The Swift keychain methods address
this app's own UUID and registration records; they do not enumerate other apps'
secrets. JADX inspection of the bundled Android classes agrees with their
notification source: JSON notification content and `getText()` serialize model
fields, and `setBody()` sets the notification data. Build plugin file copies
prepare icon/sound assets. These are consistent with the package's purpose.
The consuming app, notification contents and deployment permissions are unknown.

wp2shell's main guard dispatches `check`, `read`, `exploit` or `shell` after CLI
argument parsing. The HTTP client uses the operator's target/proxy; the code
constructs nested batch requests and SQL injection through `author_exclude`.
Its extractors recover results through UNION, EXTRACTVALUE and boolean binary
search. PoisonGraph constructs fake posts and changeset/re-entry relationships;
`escalate` submits a new administrator account in the batch tail, then verifies
login. The authenticated session uploads a ZIP containing generated PHP and
activates the plugin. The PHP hashes a request token, then exposes command
execution, request-selected stream reading and request-selected file writing.
The client extracts command output between markers and offers explicit cleanup.
All original hostile/suspicious findings describe this real generated shell and
remain. The new SQLi and file-management detections describe additional real
functions. A security engineer should recognize this as an offensive tool;
authorization for any actual use and whether an encountered host is an operator
workstation are unknown. This archive is not itself an installed victim-side
webshell. The upstream CVE/version claims were not tested on WordPress servers.

The native executable's configured mode is 3 at VA `0x404120`. Entry reaches
`0x401cb0`, which calls `0x401900` for that mode and then `0x401390` for cleanup.
The former builds an Active Setup key, writes a REG_EXPAND_SZ `StubPath` at
`0x401a4b`, reads its own image through CRT I/O, patches the copy at
`0x401aca`/`0x401b0e`, writes it at `0x401b26`, and creates a process.
The alternate mode-1 path extracts resource `DLL/101` to a System32 DLL and
calls `0x401260`, which deletes LanmanServer's `ServiceDLL` at `0x401320` and
rewrites it at `0x40133e`. `0x401150` allocates remote memory, writes the DLL
path, resolves LoadLibraryA and passes it to CreateRemoteThread at `0x40123d`.
`0x401390` obtains its own short pathname, constructs COMSPEC `/c del ... > nul`,
creates a child and resumes its thread. Mode 2 also contains copied executable
service installation code at `0x401fd0`. These paths establish hostile capability
without claiming every alternate mode runs in this configuration.

The embedded image at file offset `0x5060` is damaged: DLL resource size 39,936,
no parsed imports, mostly zero `.data`, and zero instructions at its entry RVA
`0x741a`. Thus no working DDoS loop, Remcos payload, Elex component, or WannaCry
ransomware behavior is established. StormAttack attribution is corroborated by
the server/welcome names, embedded command format and installer implementation.
All four existing hostile detections and its suspicious injection detection are
retained. Installation success, privileges and the original deployment are unknown.

## Rule corrections and preservation

`review.json` records every changed finding, including archive members, and the
exact old/new IDs. Relocations preserve matchers, criticality, effective file
types and platforms. No package-name exception was introduced.

* Bare `setBody()`/`getText()` names are call syntax, not Javassist or
  accessibility evidence. Their contextual consumers now reference the neutral
  observations. Expo's notification data is the concrete benign match.
* `org/json/JSONObject` is a class-name reference, not object construction or
  host reconnaissance. The host-profile and DPAPI consumers retain that exact
  required observation through the new reference.
* Generic `postMessage(JSON.stringify(...))` is IPC JSON messaging, not a
  WebView bridge. The Flutter consumer retains its WebView-specific legs.
* `RECEIVE_BOOT_COMPLETED` text is a permission reference, not a service
  operation. Existing installer/persistence consumers retain their exact leg;
  the separate structured manifest-request observation remains distinct.
* An authorized-use disclaimer does not identify IndustrialXPL or OT/ICS.
  Its exact matcher moves to security-testing documentation; IndustrialXPL's
  identity+disclaimer exception still requires genuine framework identity.
  Removal from broad tool exclusions intentionally prevents a disclaimer alone
  from hiding attack capabilities.
* The prompt-risk regex previously treated “attacker ... inject” in SQL attack
  documentation as agent-safety evidence. It now requires prompt/instruction
  content. Real defensive prompt documentation and a live override are retained.
* Javassist's upstream JvstTest triggered the memshell generator composite using
  ordinary bytecode APIs. That composite now also requires a shell-generation
  API. The generic APIs remain visible, a shell-generator positive still
  matches, and real CommandFilterChainTransformer instrumentation-webshell
  source retains its hostile handler-patch finding.
* Boolean SQLi interpolation accepts variable names beyond `c`; the original
  form remains covered. The added UNION template requires a numeric-predicate
  breakout, false predicate and interpolated projection; an ordinary UNION
  query is a near miss.
* The new PHP write observation structurally requires request subscripts in
  both path and content arguments. Its hostile composite additionally requires
  the existing command webshell and request-selected read. An ordinary editor
  retains only the neutral write; a fixed-path write does not match.

Exact consumers and ancestor directory selectors were inspected. The remaining
`process/interpreter/` ancestor consumer is Python-scoped Empire generator
evidence, so moving the macOS WebView atom changes no supported input there.
Generic call/JSON references no longer supply accessibility, reconnaissance or
intercept ancestry by themselves. Explicit contextual consumers retain them.

## Verification and provenance

Run the focused controls outside the test tree so detector-fixture exclusions
cannot hide matches:

```
python3 testdata/triage/expo-wp-storm-first-review/check.py /absolute/scratch/controls \
  --baseline /absolute/scratch/before-traits --record /absolute/scratch/results.json
```

The checked controls include an inert constant-pool DPAPI/GCM/JSON profile,
JSON-only near miss, notification getter/setter, original/renamed SQLi templates,
ordinary SQL, request shell/editor/fixed-path writes, Flutter/worker messaging,
boot permission, disclaimers and prompt/SQL prose. Existing fixtures outside
this batch cover the malicious WordPress pipeline, Android password export,
an APK, defensive prompt examples and a live prompt override. The class fixture
tests references only; it does not implement encryption or credential theft.

External controls were fetched with forager; originals and `.forage.json`
records remain under scratch, not in the rule tree:

* [Exact Expo source revision](https://github.com/expo/expo/blob/b667d77588d2cdf13e6fb83572040dbc2bc8781e/packages/expo-notifications/src/getExpoPushTokenAsync.ts).
  The separately fetched npm tarball SHA-256 equals the submitted hash.
* [Exact wp2shell source revision](https://github.com/Crypto-Cat/wp2shell/blob/e7220d170f9e/wp2shell.py),
  source SHA-256 `54fa9d7d57f3734166719697b2340d53da7d3b617fa2ac4be232004453bc63a9`.
* [Javassist JvstTest at rel_3_30_2_ga](https://github.com/jboss-javassist/javassist/blob/rel_3_30_2_ga/src/test/javassist/JvstTest.java),
  SHA-256 `f5a11fc037d2e165c43309052feb3838c5b028367993b934672553774cbe0ff4`.
* [MemShellParty](https://github.com/ReaJason/MemShellParty) master source ZIP:
  CommandFilterChainTransformer rewrites Tomcat's doFilter to execute a request
  parameter and return process output. The fetched bytes and provenance are
  retained for replay; the moving branch is not asserted immutable.
* [IndustrialXPL README](https://github.com/mrhenrike/IndustrialXPL-Forge): genuine
  framework identity and authorization wording remain recognized.

No original attack finding is lost on any submitted archive member. The known
JvstTest false positive is the only intentionally lost suspicious finding on
external controls. Classifier results and any disagreement are in `review.json`:
the public queue's hostile verdict does not override these byte-based judgments.
wp2shell's added accurate attack coverage can raise its classifier alert while
the overall tool verdict remains BENIGN. No inaccurate rule is restored to
shape its score.
