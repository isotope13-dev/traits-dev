# Objective-C mislabeled-bad review — 2026-11-04

All 40 snapshot entries were scanned with Cleave and Atom: 37 are bad and 3 are good. Some files use an Objective-C extension but contain IRC scripts or configuration, and one is an archive.

`7a4f10c3d5cc` collects host, user and network details and sends a report by HTTP after a local gate. A new hostile finding combines those operations, and both scanners detect it; replacing the POST with GET clears the control. `62339d312108` separately reports debugger-detection findings over HTTP and was already detected as hostile. The testing provenance and local gate do not neutralize these active reporting PoCs.

`6b8bd94888c4` fetches an executable with certificate checking disabled, saves it under a hidden service name, makes it executable and launches it in the background. A new hostile finding detects that sequence in both scanners; changing the concealed name clears the control. Three generated fixtures carrying the same downloader were moved from suspicious to hostile.

`727f0643dd7a` walks files, XOR-encrypts them, removes originals and writes a ransom note. Both scanners detect a new finding that combines those operations; an altered ransom-note control clears. `01cc9d72f643` combines SSH password attempts, key deployment and remote cron execution; both scanners detect the new propagation finding.

`b029e0c661f1` captures a Photon screenshot, sends it over HTTP and writes a decoded hidden stage. `bcc61b8ab1c1` changes a Solaris service to run a network shell. `6ad9bd23eb6c` combines an HTTP beacon and command shell with cron setup and sensitive-file targeting. `4a4e6fbe5383` combines cron self-persistence, debugger detection and network communications. `ad2b96503a23` combines a network trigger with permission changes that add world-write access to sensitive paths. Both scanners identify each with a new hostile finding; controls removing a defining operation clear.

`0d468081f882` is an IRC auto-message script, `6ef2018e8de3` is an IRC client configuration, and `37404905c5d3` is an isolated XOR packing and anti-debugging helper. Their contents do not establish a malicious payload. The packing helper retains one suspicious debugger-check finding. An IRC rule that interpreted any fixed-nickname comparison as a controller gate was corrected to describe the comparison without asserting intent.

All Hopper classifications were confirmed. Full `make validate` passed: 3270 hostile, 2088 suspicious, 9437 notable and 1396 baseline fixture checks.
