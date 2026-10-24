# Beam and PXT archive review

All three samples are **BENIGN** based on their code and provenance. No sample
was executed. Network, interpreter, process and permission capabilities remain
analyst-visible; the verdict does not imply that these operations are harmless
in every deployment.

| Sample SHA-256 prefix | Identification | Hostile / suspicious before | After | Classifier before → after |
| --- | --- | --- | --- | --- |
| `82991ccd3176` | Apache Beam fork, commit `b245c9513fec` | 0 / 0 | 0 / 0 | BENIGN → BENIGN |
| `e67adc42a13f` | Microsoft MakeCode PXT 0.12.78 | 0 / 1 | 0 / 1 | HOSTILE → HOSTILE |
| `0c278be96beb` | Same PXT release, uppercase namespace | 0 / 1 | 0 / 1 | HOSTILE → HOSTILE |

Counts are distinct traits on the requested archive, including propagated
member findings. Each PXT archive also has four member occurrences of the same
suspicious WinRT grant before and after. No fetched dependency has a hostile or
suspicious finding in these scans. These are local slow scans with automatic
updates disabled and ordinary reference following enabled.

## Provenance and execution paths

* Both PXT archives contain the same 1,046 member contents, differing only in
  the capitalization of the archive namespace. Every member's SHA-256 agrees
  with Microsoft's [tagged source archive](https://codeload.github.com/microsoft/pxt/zip/v0.12.78),
  recovered with forager.
* All 4,342 common Beam members agree byte-for-byte with Apache's
  [matching commit archive](https://codeload.github.com/apache/beam/zip/b245c9513fec).
  The nine additional module-archive members are Gradle wrapper and repository
  files. The sample's `.gitattributes` explicitly marks these paths
  `export-ignore`, explaining their absence from the upstream Git archive.
  The sole upstream-only member is `vendor/sdks-java-extensions-protobuf/build.gradle`;
  the Go module archive omits the vendor tree.
* Beam's `setup.py` runs its local `version.py` and wraps setuptools commands
  to generate protobuf sources. `gen_protos.py` installs the declared
  grpcio-tools build dependency when needed, invokes protoc, and removes its
  temporary build directory. The Go container boot program obtains job
  provisioning information, materializes staged pipeline artifacts, copies
  the worker to `/bin/worker` with executable permissions and launches it
  with explicit job endpoints. These are distributed SDK operations.
* Beam's Jenkins website helper fetches RVM signing keys, pipes `get.rvm.io`
  to Bash, sources the installed RVM, and installs Ruby and Bundler for the
  website build. The retrieved RVM installer selects ordinary installation
  paths, fetches and unpacks RVM sources, supports signature verification,
  and invokes `scripts/install`. This is a real download/execution capability;
  its existing notable traits were preserved. Mutable URLs cannot establish
  the bytes served during an earlier deployment.
* PXT's AppX wrapper opens MakeCode's editor selector and grants the listed
  editor HTTP(S) origins WinRT access. Its debug wrapper opens localhost.
  Those grants cross a security boundary and remain suspicious. The model
  assigns probability 1.0 to the manifest members; that is a remaining false
  conviction of the package, not a reason to suppress accurate permissions.
* `pxtwinrt/deploy.ts` selects removable device folders by the configured
  drive-name filter and writes the compiler's HEX/UF2 output. Its download
  helper writes a temporary file and opens the default handler. `serial.ts`
  selects configured serial devices, opens them, reads device output and
  posts it to the editor. `winrt.ts` imports activated firmware files;
  `winrtworkspace.ts` reads and saves the editor's local workspace.
* `external/tdast.js` is readable TouchDevelop runtime/compiler code. Its
  eval paths initialize compiled user scripts; PXT's simulator likewise
  evaluates compiled simulator source. The long Base64 literal decodes to a
  1,574-byte PNG, not an executable stage. Beam's encoded coder-test strings
  are wire-format round-trip fixtures. No concealed hostile stage was found.

Deployment intent and historical remote responses are unavailable. The bytes
show development and device tooling consistent with the documented products;
they do not establish theft, spying, destruction, a backdoor or deception.

## Trait changes and retained coverage

The PowerShell command-text matcher formerly matched the first letter after
`IEx` in `statusMsg("IEx userAgent: " + userAgent)`. That is an Internet Explorer
browser diagnostic. The matcher now consumes the first token and excludes
identifier labels followed by colon and whitespace. It preserves variables,
quoted source, parenthesized expressions, cmdlet names and Windows drive paths.
No package-name exception was added. Both the erroneous atom and its derived
evaluation finding disappear from `tdast.js`; the archive loses only the
propagated command-text atom.

Five notable, general WinRT observations were added in their operation homes:
file reads, text writes, removable-device enumeration, serial-device opening,
and default-handler file opening. Symbol call matching rejects quoted or
commented API references. A parsed-call matcher covers TypeScript's cast
receiver for serial-device opening, whose projected call target is opaque.

Full archive comparisons found no lost supported detection. The distinct
notable counts change 1238 → 1238 for Beam, 878 → 882 for lowercase PXT, and
879 → 883 for uppercase PXT. PXT gains five capabilities and loses the false
PowerShell atom. Repeated scans expanded cached fetched-reference analysis;
those additional observations are not attributed to these YAML changes.
Beam's maximum ML probability changes 0.4653 → 0.5280 due to the fetched RVM
installer, remaining BENIGN. PXT remains at 1.0 despite the false-positive fix.

`python3 testdata/beam-pxt-review/check.py` checks actual WinRT calls against
quoted/commented references and IEX commands against browser labels. Before
and after scans of these existing fixtures retain every finding, including
all hostile and suspicious findings:

* `testdata/hostile/clipboard-irm-stage.js`
* `testdata/hostile/powershell-tcpclient-command-dispatch.bat`
* `testdata/hostile/hidden-batch-powershell-loader.js`
* `testdata/hostile/registry-agent-second-review/stdin-loader.js`
* `testdata/hostile/clickfix-os-gated-verify.html`
* `testdata/wsh-startup-operation-review/startup-cradle.js`
* `testdata/benign/js-powershell-webclient-command-string.js`

All consumers of the shared IEX atom keep the same ID and scope. The focused
controls and existing attack fixtures support the narrow prose-label exclusion;
no execution technique or accurate permission finding was removed.
