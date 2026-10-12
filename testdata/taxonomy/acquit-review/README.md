Second review of registry-collected samples
=========================================

All three samples retain MALICIOUS judgments based on their code, without
reputation evidence. Run `python3 testdata/taxonomy/acquit-review/check.py`
from the repository root to exercise positive and near-miss rule controls.
The checker uses test-rules because transparent OR composites are intentionally
filtered from standalone JSON output. Archive fixtures are staged outside
testdata to avoid fixture-name IP exclusions, then checked across all members.

The AES/PBKDF2 stub sleeps 25 seconds, decrypts a managed byte-array resource
using AES-256-CBC and PBKDF2-HMAC-SHA1 (1,000 iterations), then loads the
result with AppDomain.Load and invokes Stub.Program.Run dynamically. That
DLL decrypts another resource with the same algorithm and hollows a suspended
32-bit Framework/RegAsm.exe using thread-context replacement, remote writes,
and ResumeThread. The recovered payload identifies itself as njRAT 0.7d Horror
Edition; its command dispatcher includes keylogging, surveillance, defender
interference, and destructive commands. None of the outer YAML matchers can
see the encrypted child, so they describe the visible resource/crypto/activation
references rather than falsely attributing those child capabilities to the stub.
The earlier fixture comment calling this NanoCore was incorrect.

The extension claims to manage history, but a persistent background script
polls clipboard text, chunks changes, and beacons URL-encoded chunks. Its
wallet UI forwards textarea content after a debounce; sendData spreads that
input into a JSON beacon. Neither routine implements history management or
wallet-secret validation. The manifest explicitly declares required collection
as ["none"]. Omitted disclosure and an empty required list are not this claim.
The privacy controls retain the same clipboard workflow and compare an
explicit denial with empty/omitted declarations; their endpoint is reserved
example.invalid, and no specimen code is executed by the tests.

The fax script sends a public LogonMessage-to-ConfigEditor request and a fax
selector containing traversal to /usr/bin/bash. It returns a command-argument
setting (-c id); it does not submit that setting or prove successful remote
execution. It is an exploit fragment, not a completed execution trace. Rules
now describe the configuration text and keep it separate from process creation.

Placement and reference audit
-----------------------------

* ResourceManager's image-leaf matcher was consolidated into the canonical
  resource matcher, preserving standalone/getter spellings and rejecting
  native ConcRT RTTI. Both image composites and their exact consumers were
  updated. Ancestor image selectors intentionally lose this generic resource
  fact; resource selectors intentionally gain the getter/DLL/C# scope. No
  bitmap or pixel evidence was relocated.
* The mapped-image-size atom moved from overlay to layout/size; its only exact
  consumer retains the same conjunction. Broad layout selectors retain it,
  while overlay selectors no longer gain an unrelated image-size observation.
* Fax command arguments moved from process creation to process/argument/option.
  Its only exact consumer follows the move. Generic method/body-traversal
  facts moved from exploit/access-control to HTTP verb/body capabilities;
  the DNS-rebinding objective references the neutral co-occurrence composite.
* The KDF resource profile moved from fileless/managed to anti-static reflection.
  AES-decryptor and invocation references are required. A co-occurrence matcher
  cannot prove an absence of disk writes. The two remaining resource objectives
  require this sharper profile instead of bare AppDomain/Load/CreateInstance
  tokens on the metadata-token alternative; other activation alternatives stay.
* Filename-mismatch resource convictions were removed: a collector can rename
  a file without changing its behavior. Neutral provenance findings remain.
* The code-entropy matcher was renamed from native-code to code-region entropy,
  preserving all exact consumers and scope. Managed .text also contains resources;
  its entropy does not describe native instructions. High entropy is notable,
  not a property shared by virtually every PE/Mach-O binary.
