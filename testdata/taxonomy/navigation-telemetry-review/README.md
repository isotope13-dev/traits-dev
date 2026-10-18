The timestamp-only navigation control must have zero suspicious or hostile
findings. A UUID helper, navigation callback, storage write, alarm and POST
are useful neutral observations; they do not establish reachable identifier
creation, browsing URLs in storage, or a source-to-send theft chain.

The no-navigation control omits one required observation. The two identifier
controls preserve the relocated matchers. Follow, unfollow and both-operation
controls ensure that FOLLOW is a whole operation token, while preserving the
positive when the two operations coexist.

The low-whitespace observation moved from padding to the existing text-shape
profile leaf, with its matcher, defaults, exclusions and consumers preserved.
It measures a whole-file whitespace fraction, without proving compression.

Second-review conclusions:

- a80c4b152a0d: BENIGN timestamp telemetry example. `noteNav(url)` discards
  its argument and records only `Date.now()`. `ensureInstallId` has no caller.
  The four-hour alarm sends stored timestamps and an optional existing ID.
  Neither URLs, page content, credentials nor remote execution are present.
- d84df964146c: MALICIOUS AES-CBC/PKCS7 PowerShell loader. Offline decryption
  produces 1,090,973 bytes of PowerShell, then repeating-key XOR and Base64
  recover a 45,568-byte managed DLL. `FILES.WHORE.LAUNCHER` invokes a helper
  that creates a suspended hidden process (flags 0x08000004), reads PE header
  fields, allocates remote executable memory, copies headers and sections,
  replaces the thread entry context and resumes the thread. Its target is
  aspnet_compiler.exe. The script supplies a 283,648-byte embedded PE, but
  initializes that array after its first invocation, so the first attempt
  can fail; the loop can retry after initialization. Existing two hostile
  loader traits accurately describe the outer layer. No family attribution
  is justified solely by the supplied antivirus names.
- ef9a9392d6f1: MALICIOUS Baileys newsletter socket modification. The archive
  contains just newsletter.js, without its imported siblings or manifest.
  When used in its intended socket tree, the constructor schedules an
  unconditional helper that waits five seconds, fetches a mutable remote
  JSON roster, and follows its entries through the authenticated socket at
  ten-second intervals. Both inner and outer errors are discarded. Callers
  supply neither these channel IDs nor an opt-in. This is remote-directed
  account manipulation, separate from the legitimate caller-driven APIs.

The two telemetry composites moved into application telemetry at notable,
with their scopes, exclusions and evidence sets retained. Their two PRNG
support atoms moved into the existing standard PRNG leaf, and their sole
remaining explicit consumer was updated. No consumer references either
retired telemetry composite. The whitespace move preserves all eight exact
consumer references. Compact and spaced source controls exercise its threshold.

Use `cleave test-rules` for the whitespace controls: baseline findings with
no fired composite consumer are stripped from ordinary scan output. The
`evaluation_*` fields record rule evaluation, independently of emission.

The byte-identical extension-install-telemetry.js fixture is reclassified from
hostile to benign in expectations.toml; its regression requires both neutral
telemetry findings and zero hostile or suspicious findings.
