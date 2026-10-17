# Password export and hidden staging controls

Run from the repository root:

```sh
python3 testdata/taxonomy/password-export-and-hidden-staging/run_cases.py
```

The Kotlin controls bind the password-tested node to its text read, the JSON
record to serialization, and the sending receiver to a declared WebSocket.
Different node, record, and channel names (including matching suffixes), a
negated password test, local logging, and ordinary text inputs must not export
passwords. Renamed identifiers must still match. WebSocket imports must not
imply an OkHttpClient type reference.

The shell controls require the same variable for hidden filename assignment,
wget output, chmod target, and background execution with stderr discarded.
Mismatched variables, visible names, foreground execution and visible stderr
must not match this precise chain. These are suspicious observations: legitimate
self-updaters can use the same mechanics.

## Reviewed samples

- `6da44858f5c0`: reconstructed Android accessibility collector, MALICIOUS.
  `onAccessibilityEvent` visits the active UI tree recursively. Under a positive
  `isPassword()` test and secure-keyguard check, `snapshot` reads the same node,
  inserts its text into a JSON record and sends that record through the typed
  WebSocket. `enroll` pairs to localhost ADB using TLS 1.3, exported keying
  material and SPAKE2, then requests WRITE_SECURE_SETTINGS through the shell
  service. The abstract transport implementations and connection endpoint are
  not supplied; no remote-command dispatcher is claimed. U+200D separates the
  letters of its display label; removing those characters reveals FuturePortal.
  Add Kotlin export coverage and extend the existing exporter/elevation rule.
  Move the WebSocket import from HTTP to WebSocket client; narrow the broad
  okhttp3 package matcher to the actual OkHttpClient type.

- `d23bf440668e`: Sora/Mirai multiarchitecture bot downloader, MALICIOUS.
  The shell maps uname/cpuinfo to architectures, selects hidden temp staging,
  retries wget/curl/BusyBox against the same architecture URL, chmods its hidden
  output and backgrounds it with stderr discarded. It does not itself contain
  the bot's C2 or scanner implementation. A read-only retrieval of its exact
  x86_64 URL returned ELF SHA256
  `3bc067959aae3f2b1f8ec1efcfbd380524660de9b3f3bc0c7a32cc82516a5c5e`.
  Rizin traces main's C2 receive at 0x401d9d into attack_parse at 0x401de4,
  which dispatches attack_start at 0x402e86. The UDP attack repeatedly calls
  send at 0x407b70. resolve_cnc_addr at 0x410280 configures 37.16.74.19.
  These bytes were never executed. URLhaus independently records the exact
  server and Sora payload paths: https://urlhaus.abuse.ch/host/2.27.203.59/ .
  Live payload bytes corroborate the current delivery endpoint; they do not
  establish an immutable historical payload. Remove the overbroad hostile
  C2/dropper rule; replace it with bound execution and hiding observations.

- `61a9c186a307`: Eupdate Helper 4.0.1, BENIGN.
  Rizin traces 0x412964 fetching version/downurl metadata, checking the version,
  prompting with MessageBoxW (0x412c6e), and requiring IDYES (0x412c77) before
  downloading and swapping its own image. The same function checks MZ and
  removes invalid downloads. 0x413f30 locates ESET ecmd.exe and launches /update.
  0x415c80 obtains upstream accounts; 0x414868 relays ESET update resources using
  Basic authentication and filters manifests. Signature-resource HTTP 404s do
  not by themselves establish malicious update substitution. The local port
  owner termination frees its listening port, not a named security process.
  0x416bb0 decodes strings as byte XOR key XOR ((31*i+7)&255); decoded fields
  are encrypt/type and endpoint https://id.1yz.me:4046/id.html, not stolen local
  credentials or a command channel. TLS callbacks are MinGW runtime handlers.
  0x4127e4 opens its image, seeks EOF and appends random bytes; standby handoff
  permits this while the main image exits. Retain the accurate suspicious
  self-hash-rotation rule and notable network/autorun/update observations.
  Clarify the exit diagnostic description; no product-name exception added.

The standalone files have no fetched package dependencies requiring PURL tests.
