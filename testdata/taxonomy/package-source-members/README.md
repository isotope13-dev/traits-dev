# Stranded member detection corrections

Run `python3 testdata/taxonomy/package-source-members/check.py` from the repository.
Fixtures are inspected as data; none is executed or fetched.

The reviewed members are two inert npm manifests, 38 unchanged HashiCorp HCL
v2.24.0 source files, and errwrap v1.1.0's error-wrapper tests. Each Go member
was compared byte for byte with its published Go module source. All 41 members
have individual BENIGN markers beside their extracted files, outside this repo.
The confirmed archive judgements are unchanged.

| Correction | Required evidence and nearest counterexample |
| --- | --- |
| Puppeteer dependency belongs in manifest metadata | A runtime dependency field names puppeteer-core; it does not identify a PDF extension. The extension still requires its package and publisher identities. |
| Short description counts as present | Any non-whitespace description excludes the undescribed ISC finding; a missing description retains it. |
| Repository root is metadata | A git declaration with a host-root URL establishes incomplete provenance, not supply-chain intent. A root has no repository name to mismatch. A real differently named repository retains the mismatch. |
| Datagram sending requires a UDP method | WriteToUDP and WriteToUDPAddrPort specify UDP. io.WriterTo's WriteTo also serializes tokens into memory or arbitrary writers. |
| Generic writes use the existing stream home | The Go Write/WriteAt matcher, Go scope, notable level and 0.65 confidence are preserved. All three exact consumers were updated; no directory consumers of the old write or new stream leaf exist. |
| Explicit Go generators are build declarations | The structured generator argv remains unchanged and notable. Its exact objective consumer now uses metadata/build/config. Naming x/tools in generator argv records tooling, not library identity. Existing source-archive identity remains available. |
| Model evaluation needs model context | LLM/language-model output or response near evaluated supports the observation. Returned HCL values evaluated by a config interpreter do not. |

`cases.json` records moved IDs and both positive and nearby negative fixtures.
The hostile shell-generator fixture verifies preservation of the relocated
build declaration's objective consumer. The full member rescan found zero
suspicious or hostile findings.

Known engine limitation: common_controllers has empty preinstall/postinstall
strings. Its existing inert-script YAML findings correctly describe them, but
Cleave's built-in install-hook findings still say they run during installation
and add new-package-with-hooks. RULES.md identifies these as engine-generated
facts that YAML cannot override. No duplicate shadow rules or identity-wide
suppressors were added. Correcting their wording requires an engine change.
