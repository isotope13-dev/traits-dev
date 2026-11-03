# Wheel mislabeled-bad review

The snapshot contains 41 files: 40 wheel files and one ZIP archive, including
one wheel recovered after the original snapshot. Both scanners have scanned
all 41 files, including the larger archive. An initial
scan is not a classification,
and a package's distribution name or collection label is not evidence of its
behavior. The previously missing wheel
`360a1fbed512aa82246977b76f2a8bc1ccfc794b79bd23f39f35c62d1502675a`
(`data-proxy-for-test-0.1.1`) was recovered from PyPI and verified against its
Hopper SHA-256. The verified bytes were restored to the review snapshot and
uploaded to Hopper, which cleared its missing status.

`360a1fbed512aa82246977b76f2a8bc1ccfc794b79bd23f39f35c62d1502675a`
(`data-proxy-for-test`) copies the identity and layout of the legitimate
`mcp-proxy` project, while adding a `.pth` file that imports its cache module
at each Python startup. That module immediately fetches two named files from a
configured cloud-storage bucket into a home-directory cache. The recovered code
explicitly refuses to execute the cached files; the scan must not claim an
execution that is absent. The exact wheel digest is also independently listed
in [OSV MAL-2026-10642](https://osv.dev/vulnerability/MAL-2026-10642), whose
source analysis identifies the unexpected startup staging added to the copied
project. This is a malicious supply-chain staging package; Hopper retained
**bad** and confirmed the recovered bytes. A bound source-level observation
now follows the import-time call chain to a named downloader; two suspicious
findings accurately report the bucket/cache context and archive co-occurrence
with a startup hook. Both scanners agree and uncached validation passes.
General cross-file linkage between a `.pth` import and its module, and between
the named downloader and its implementation, remains a detection gap; the
co-occurrence findings do not assert those connections.

`2556855234f6570def02ffbe93e560c64eca2926cb65f042e2e81f34bc6b22d9`
(`mpl_presentation_styles`) installs a sourceless bytecode
preloader through a `.pth` file in a specific managed environment. Static
Python 3.12 bytecode disassembly, without executing the sample, shows an audit
hook that reads file contents into a queue and a separate network sender. The startup
trait is hostile, and existing neutral bytecode observations report individual
audit-hook, read-only-open and HTTP-authentication names. These names alone do
not establish data flow; synthetic name-only fixtures show why their
co-occurrence should not be treated as suspicious by itself. Both scanners
report the startup hook and Hopper confirmed **bad**. Automatic bytecode
data-flow coverage for the collection and network transfer remains a gap.

`81f0d1291a975d012d1b892cf9967557fdbb1ad4e1ac0545702ad235ace1cac5`
(`mrmustard`) starts a worker on import that collects credential-related
files, uses encoded HTTP, writes a `.pth` process launcher, and prepares a
recurring cron job. Both scanners detect the credential and bound `.pth` write
as hostile. Proximity-only `.pth` and cron observations were reduced to
suspicious, because they do not independently prove the data flow. Hopper
confirmed **bad**.

`694e65589583` (`coreason_manifest`) has two prompt-override observations in
`ontology.py`. Both originate from one explicitly labeled synthetic payload
inside a schema's examples, rather than from an instruction being sent to an
agent. The wheel has 11 members, including five Python files. Static AST
inventory found no direct `open`, shell execution, socket, subprocess, or
pickle/marshal deserialization calls in those files; the base64 operations examined convert
vector data for numerical comparison, and the AST parsing examined validates
input rather than executing it. A further review of the schema's instruction
and security-related text found the override phrase in the labeled example;
other matched security references describe validation or policy fields. A
structural observation identifies the labeled
synthetic instruction in the schema examples without suppressing prompt
findings. Both scanners report the context in the wheel, focused tests verify
that a separate live prompt remains visible, and uncached validation passes.
The two suspicious observations describe distinct portions of the same example
and remain visible. The included library is **good**, and Hopper moved it to
that label. The current Cleave scan produced 12 records with 3 analysis gaps;
Atomscan produced 8 records with the same 3 gaps.

`884929e56cfa4785f67ea49d26f8c0d26794e84a64f3b04d71c9361d85a187ce`
(`mult_flow`) writes a hidden Startup script when its multiplication helper
is called. The script decompresses and deserializes a pickle. Static inspection
of the pickle operations, without deserializing it, recovered source for a
socket-to-PowerShell relay. The archive scan reports the startup-persistence
trait but does not recover the serialized payload. A guarded socket-to-stdin
rule now detects the separately recovered source in both scanners. Uncached
validation passes and Hopper confirmed **bad**; automatic recovery remains a
coverage gap. A recovery path must distinguish data-only examples from source
that actually reaches a loader before inheriting child findings.

`27512ee5687e` (`eth_security_auditor`) runs a silent curl command on import
and passes its output to `node -e`; three hostile traits describe this loader.
Both scanners agree on those findings, and Hopper confirmed **bad**.
`9116c9a2129259d93b6bfaf8ec46501ca1d420991324c94ee52d701570a71384`
(`defi_risk_scanner`) and
`ebad1e3186132b2892da38a92fb38e0e6e697e53e080adb8d2fbb899b93dc8ec`
(`cryptowallet_safety`) use the same import-time curl-to-Node pattern. Each
scanner reports the three hostile loader traits; Hopper confirmed **bad** for
both.

`2d42344135f6e29f071bd7bd555fa546dd56e6dd86b513d8671302e1ba1b20fe`
(`dementor`) implements an IPP response carrying a configurable Foomatic
command-injection directive. A new source-level rule detects the response
construction in addition to the existing third-party exploit signature; both
scanners agree and Hopper confirmed **bad**.

`561eea6f1b2e2f3e9834682d2f2dab4a651d8be4f6c31563e463da323b351ee1`
and `a631cc6e6f60470c71983057810681f2bec9278b5a2421cab93ca842ba78ff7d`
are versions of `linksiren`, a dedicated tool that creates UNC credential
lures and deploys them to remote shares, with EFS RPC trigger functionality.
Both scanners report the lure, and Hopper confirmed **bad** for both. Two
additional SMB findings now describe file/archive co-occurrences as suspicious
instead of asserting an unproven connection between the operations.

`251902a7a156ff0986f488b9d33051149fab99bb5df44707779f1103f93bb589`
(`fantasy_hockey_notifier_cdk`) includes a JSII archive with 5,747 members.
Its own JavaScript retrieves a configured ESPN cookie from AWS SSM with
`WithDecryption`, reads league events from ESPN, and sends notifications to a
configured SNS topic or Discord webhook. The 106 bundled dependency manifests
had two prepare scripts (Husky and a MIME build); review of bundled code for
credential and process-execution patterns did not identify an attack. The SSM
observation now recognizes both singular and plural parameter commands while
binding decryption to the command object; a boundary test covers that change.
Fresh Cleave and locally built Atomscan scans found no suspicious or hostile
traits, with 5,754 and 5,452 records respectively; Atomscan reported 2,526
records with analysis gaps. Uncached validation passed, and Hopper moved the
wheel to **good**.

`985ada2bb71018594b9b1b944dd6f9f326ef0914c08804d7a39abe8e7bc0a39d`
(`baidubsrc`) contains one inert greeting function and distribution metadata,
with no install or startup script. Neither scanner reported suspicious or
hostile traits; Hopper moved it to **good**.

`081ca1d3213e0fdea322b9bb8ef23fdc0dc04f7f36eb20d94e223997c3e4a2c6`
(`pafex`) is a configuration library that deserializes caller-supplied pickle
data before checking it; this unsafe feature is its one suspicious finding.
`b5f29b18ff95ce48bf076a3851ebdb10915025f60bbb1fcdd88fda0b394f806b`
(`vsecret`) offers a substitution encoder and executes caller-supplied decoded
code, also reflected by one suspicious finding. Neither implements a specific
attack or runs those operations on import. Both scanners agree and Hopper
moved both to **good**.

`d4971d270fb5d919ee6e9636f45fdc0b0ac645f15bc9ed31b8673ab00f64b361`
(`stepscribe`) models state machines. Its JSON loader evaluates a selected
state-type value with Python `eval`, which is unsafe for untrusted input;
a new notable observation records the subscripted argument. The library does
not itself implement an attack, and Hopper moved it to **good** after both
scanners agreed.

`479a481cb4d67b9df4e530610b1de460879aa79f746c5e1a2e6b49164a3919fb`
(`lognexis`) provides opt-in request logging middleware and a network client.
The middleware includes all request headers in the log record, which can
expose credentials to the configured logging service; existing observations
surface header copying and logging. Both scanners found no suspicious or
hostile traits, and Hopper moved it to **good**.

`810821b323428ed46cb956ecd194e3be666de3f75777e725f90298febc8383ec`
(`llm_interview`) installs opt-in coding-agent instructions for recording and
submitting interview conversation history to a user-configured service. Both
scanners now report the history-collection wording as a neutral observation;
the package does not automatically submit unrelated files. Hopper moved it to
**good**.

`07a919b154fcb36c952ff28809308254eb11316cc93c5b93562c47a8b580044d`
(`plugin_scanner`) contains security scanning and policy-enforcement tooling
for agent plugins, including optional MCP verification and a monitoring UI.
Neither scanner reported suspicious or hostile traits. Hopper moved it to
**dual-use** under the security-scanner classification policy.

`72d8f4009509bf3fcfa6475f9d8bc24c80b919b0fa40127ee0eefcdd63aa9d1e`
(`hol_guard`) is related security-scanner and agent-guard tooling. Of its 94
Python files, 83 are byte-identical to the reviewed plugin scanner; the
remaining changed and added files were inspected separately. Neither scanner
reported suspicious or hostile traits, and Hopper moved it to **dual-use**.

`a63bd593b785d3f95467cc9ff1504d349e78e0451b8facd111394af21306a6fa`
and `a759516f2c80e38cbb9bc18f7ebbed9b36852b7c5651c059a84e9be16c66a75b`
are versions of the `authfort` authentication library. Their Python source
differs only in the declared version; the code implements authentication,
OAuth providers, persistence, and framework integration. Structural inspection
of the source members and both scanners found no suspicious or hostile
behavior. Hopper
moved both to **good**.

`2defb7a1599e90bdb801be43c698b536c5a60dacb4a469584b8ccb452233e35a`
and `75e11407bf24f045e32ef26b5e753f49f64fee822c8c9bfc5184a0911cb0969c`
are versions of the `durabletask` client and worker SDK. Structural review
found orchestration, gRPC, serialization, and testing code, with no observed
attack implementation. Both scanners found no suspicious or hostile traits;
Hopper moved both to **good**.

`597a31a37aae93e81e1bb5c227b7f66e17f948dd6d64887789ec7bc39ba0dd63`
(`boto3_stubs`) consists of type stubs and distribution metadata.
`fe8c51b8ded5c76db268bfc01b27db66b8de5a071bb637ee0ec57650433d66c0`
is a generated Pulp API client. Structural inspection and both scanners found
no suspicious or hostile behavior; Hopper moved both to **good**.

`11970be1fc26cd47463e6b50423fcc3b41a39ba7733a7fabfdd073274011d584`
(`suite2p_haisslab`) is a scientific-imaging package. It loads NumPy object
arrays with pickle enabled, which is unsafe for untrusted input; both scanners
now report that option. Static inspection of its bundled array pickles found
only NumPy reconstruction and codec globals. Neither scanner reported
suspicious or hostile traits, and Hopper moved it to **good**.

`9fc236bacc1f0cfae4bd8a805e0b9297a5541fd9d397ab2f98b314d80c32b50f`
(`agi_page_geospatial_3d`) is a mapping UI. Its `eval` calls select from a
fixed list of local variable names, and the new subscripted-`eval` observation
reports them without asserting attacker control. Both scanners found no
suspicious or hostile traits, and Hopper moved it to **good**.

`fd37d15f077375f77cbfbbb57abed6b2c6ae0a3db39cf4815400742441b3b60a`
(`mistralai`) is an API client with generated request and model modules.
Structural inspection of its 467 Python files found no `exec`, `eval`, or
subprocess calls. Neither scanner reported suspicious or hostile traits;
313 records had flow-analysis gaps. Hopper moved it to **good**.

`ae25c0e39831e8a5ff1be43ceffc0d4c30b8b0bc90662999294ae8265c1eea77`
(`workpilot`) is an AI assistant with shell, browser, MCP, cloud messaging,
and web UI features. Structural review covered its Python modules and bundled
JavaScript, with closer inspection of process launch and network functions;
no dedicated attack implementation was observed. A generic occurrence of
“repair” had been mislabeled as an exploit-retry loop, so that observation and
its co-occurrence composite were corrected. Neither scanner now reports
suspicious or hostile traits; 294 records had flow-analysis gaps. Hopper moved
the package to **good**.

`0b6e5f53f11d3005787e206d9c03382f459ef048a43c544e3db3b1e05a961548`
(`num2words`) contains number-to-text conversion and language modules.
Structural inspection found no process execution or network imports, and both
scanners found no suspicious or hostile traits. Hopper moved it to **good**.

`0dc9d2987185448bb41de0f6e5f26e6d9b1b03358bf88d12cb67b06c99297949`
(`nikobus_connect`) implements home-automation protocol, discovery, and
configuration handling. Structural inspection and both scanners found no
suspicious or hostile behavior; Hopper moved it to **good**.

`9e355bacc25022803f2de47ee4214c39726b6bead81b9dccdc9a4db8c0293a5a`
(`executor-http`) provides a configurable remote job, file, and proxy service.
Its file-path containment check compares absolute paths as strings, allowing
a sibling path sharing the root's prefix to pass that check. A new neutral
observation describes the comparison in both scanners. Hopper moved the
general-purpose remote service to **dual-use**.

`db3ce77c60ffdc8b6c6a82d76b5b935de61b96de3ff8ae50c9101119bc369b39`
(`django_resaas`) is a SaaS framework with token-checked deployment endpoints.
Its rollback code interpolates release paths into `os.system` commands,
which can be unsafe if those paths are attacker-controlled. A new neutral
observation reports the interpolated shell command; both scanners found no
suspicious or hostile traits, and Hopper moved the package to **good**.

`8a65aab24347699ae9872be9ba8789da7c0c1de5321be09a9e0f8397016872f9`
(`arthub_api`) is an SDK with example scripts. Its CLI loads a user-selected
Python configuration via `compile` and `exec`; existing notable findings
describe that behavior. The examples include login and account-export
operations, with no observed attack implementation. Both scanners found no
suspicious or hostile traits, and Hopper moved it to **good**.

`3e3edb4dfe46d0875cf579f7c1451b344ea39b25256b3f5faace643f25e51ea9`
(`pyverse2d`) contains game and rendering modules and a font. Structural
inspection found no network or process-execution imports; its `ctypes` use is
in renderer modules. Both scanners found no suspicious or hostile traits, and
Hopper moved it to **good**.

`b369c932d69cd1f1356a31c92aa6153570c1827c0179a9634e3250e4d6e17fa1`
and `d54056a72546a43cf0089201cd5b26677d513668b24576c4b4c2641d90559a3a`
are related log-upload libraries. Their documented, explicitly called API
recursively reads `.txt` and `.log` files, by default under the Windows drivers
directory, and posts their contents to a configurable service. They perform no
upload on import. Both scanners report the file-search and POST characteristics
without suspicious or hostile findings, and Hopper moved both to **good**.

`01133e09978a1c6a9855c5b27c6f761ea537c2044a0affccc9762adb6efc61b5`
and `55ac47c58de94e03d1171baa828ce270d9c229778c305a3d89a42108fa7ed932`
contain identical Gemini client code with a hard-coded API credential and an
import-time interactive loop. The code does not implement credential theft.
The duplicate observations were made notable, retaining one suspicious
credential-exposure finding; both scanners agree and Hopper moved both to
**good**.

The larger archive `b7062077c164` is a Windows Python installation. Atomscan
initially reported a hostile screenshot/exfiltration composite in a bundled
`mfc140u.dll` from DPAPI, GDI, and WinINet API co-occurrence; the composite was
moved to a neutral profile because those APIs do not prove exfiltration. A
separate wheel-wide startup-hook/exit co-occurrence likewise did not establish
that the hook reaches the exit and is now a neutral archive profile.

Static provenance checks matched 34 unmodified files to the official Python
3.12.10 embedded distribution; its modified `_pth` enables the bundled site
packages. Of 33 installed distribution RECORD files, 31 matched published PyPI
wheel records on 2,420 common hashed entries, with no differences. The two
source-only packages' Python files matched their published source archives.
The 100 Python files in `Lib/distutils` matched the bundled setuptools copy,
and 431 files in the `get-pip.py` payload matched the published pip 25.0.1
wheel. The only unmatched launcher was the vendored pip launcher with a small,
ordinary `wheel.cli` entry point. Three unrecorded fernet package files were a
one-line import and copies of its upstream module and setup file. These checks
and review of the installer establish that this is a general-purpose Python
runtime, so it is **good**; Hopper already had that label. Fresh scans found one
suspicious credential-manager API finding in the `win32cred` binding and no
hostile findings. Cleave represented 11,907 records, Atomscan 5,160, with
1,872 records reporting analysis gaps in each; uncached validation passed.
