# C# mislabeled-good review, 2026-11-04

The 40-entry queue was scanned locally in slow mode without reference following;
preliminary results are in `/var/tmp/csharp-good-initial.jsonl`. The queue
includes standalone decompiled source fragments and archives, so endpoint
rulings are based on the contents of each artifact, not names or comments.

`9665b5e0c95a` is an executable staged-loader example. It gates execution on
uptime history and debugger state, downloads HTML containing a hex-encoded
executable, writes it locally, registers it under a Run key, and starts it.
Its endpoint is deliberately nonfunctional, but the executable attack chain
is present. A new hostile observation ties the download, decoding, file
write, Run-key registration, and launch; the existing uptime-gated-dropper
observation supplies a second hostile finding in a different directory.
The original matches; controls without the Run key or launch do not. A fresh
no-follow scan reports both hostile traits, validation passed, Hopper moved
it to bad, and the hash-verified snapshot was relocated.

`a460da78ba35` implements a Luckyware loader-builder server: it copies loader
source templates, inserts owner and build identifiers, invokes MSBuild, and
uploads compiled results. Its templates are external to this source fragment,
but the implemented builder is dedicated attack tooling. A new hostile trait
reports the build-and-upload workflow; existing Luckyware traits provide the
second hostile directory. The original matches and controls without compilation
or upload do not. The fresh scan reports both, validation passed, Hopper moved
it to bad, and its hash-verified snapshot was relocated.

`f941136e62b5` is a decompiled runtime fragment that reads its own executable,
decodes and decrypts a stage, passes it to a PE helper, hides its form, copies
itself, and writes a machine registry value. The registry path is obfuscated;
no specific persistence key is inferred. Two new hostile traits report the
stage handoff and the separate hidden self-copy/registry behavior. The real
source matches both; removing the handoff removes both, and removing the
registry write removes the latter. The fresh scan reports both hostile traits,
validation passed, Hopper moved it to bad, and its snapshot was hash-verified
and relocated.

Seven other decompiled fragments from the same provenance contain generated
resource helpers, a stream-decryption utility, an assembly-resource resolver,
or a module dispatch whose target is outside the fragment. Malware-naming
comments and assembly metadata describe provenance but do not establish that
each isolated fragment is itself hostile. Their provenance and dispatch
observations were downgraded to notable; the assembly resolver retains one
suspicious resource-loading observation. All seven have good endpoint rulings,
with validation and Hopper confirmation.

`f222787add83` is a RustPlus desktop client source file. Its former logic-bomb
finding combined date conversion, process launch, and child cleanup in
unrelated code. The unsupported combination was relocated to neutral
co-occurrence traits, and a separate rule requires a real time gate before
self-deletion. A control with a time-gated self-delete matches; one without
the gate does not. The fresh scan reports no severe findings. Endpoint ruling:
good; validation passed and Hopper confirmed the label.

Twenty-five other standalone source files were reviewed as their actual
contents: packet data classes, generated forms and resources, development
tests, a certificate-pinned network helper, a local extraction utility, and
other supporting classes. They contain no standalone executable exploit or
malicious implementation. Fresh local no-follow scans report no severe
findings; validation passed and Hopper confirmed all good labels.

`2dc0289a02bd` is GlassIt, a VS Code extension for adjusting window
transparency. Its code invokes PowerShell or window-management commands for
that purpose. The fresh local no-follow scan reports no severe findings;
validation passed and Hopper confirmed the good label.

The remaining source archives were reviewed and recorded good. `10f779163943`
(Playnite) and `2cf2d2cab49a` (EverythingToolbar) contain application source;
searches for executable exploit indicators and fresh slow scans found no severe
traits. The previously unknown EverythingToolbar snapshot was hash-verified
and moved to the good pool.

`58b4ed9bb4ee` is Selenium source. Its GitHub credential helper reads local or
environment credentials and uses a substring check for the intended service;
this is one justified suspicious warning. A second finding had incorrectly
applied an x86-64 gadget rule to an embedded IBM S/390 library. A scanner fix
now recognizes S/390 rather than mapping it to all architectures; a Rust
regression test and a fresh scan of the actual library confirm that the x86
finding no longer applies. A full archive scan reports only the credential
warning. Repository validation passed and Hopper confirmed all three labels.

C# total: 37 good and 3 bad.
