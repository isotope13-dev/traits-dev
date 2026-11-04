# VB-family bad-label review, 2026-11-04

The snapshot contains 40 items, including VB.NET, macros, MOF subscriptions, archives and an executable. Classification is based on the contents, not the containing project name. The initial scanner output is `/var/tmp/triage-vbs-scans.jsonl`. 

## Confirmed hostile

- `9f8c29e12a1a`: loops a threatening message box indefinitely.
- `2c0fcd96aa6b`: constructs a remote script moniker and passes it to `GetObject`.
- `537cd0445640`: workbook-open macro decodes the author property into a hidden shell command.
- `20ebb1b034b0`, `8d91bff3211e`: timed permanent WMI subscriptions execute local account creation and administrators group modification commands.
- `7dc3d0bdd070`: invisibly starts an adjacent executable named `svchost.exe` while opening a PDF decoy; the executable itself is absent.
- `dca8f6719aea`: macro runs a command assembled from cells (existing hostile detection).
- `b8133fadef0b`: reconstructs formulas into a hidden Excel 4 macro sheet and executes them.
- `02045517a629`: disables Word virus protection and copies autorun macros across documents and templates.
- `14436739f0a1`, `637db53b0766`: document-open macros decode form content to disk and launch it with `CREATE_NO_WINDOW`; the form content is absent.
- `22926d2fc7e3`: auto-open macro activates an embedded OLE package and runs a macro from a hidden extracted document.
- `54bce5df9b9e`: WSF loads a remote script among dozens of long, repetitive padding comments. The remote content is absent; the finding describes the obfuscated remote loading, not that content.
- `fa1063a1de74`: removable-drive autorun worm (existing hostile detection).
- `e2fa18eaf6aa`: loads an embedded Wi-Fi password collector, invokes it and sends its results over a socket. This directly covers the requested hostile host-findings behavior.
- `477e4aee7cf7`: encrypted remote controller receives keylogs and passwords and issues execution commands.
- `b4cd01f15e6d`: copies a WebDAV ZIP, extracts it, silently registers a DLL and deletes its generated batch launcher; the remote archive is absent.

Each new finding above was checked with both cleave and atomscan against its original and a control with a necessary behavior removed; the finding cleared on the control. Scanner exit status alone is not used as the label.

## Good

`493adba75cb8`, `5b2610ada340`, `66a2d4d36165`, `273066351c11`, `5d24d1fe402c`, `08f3b3e7e2ac`, `bee62ada7071`, `17ee0458fece`, `3172e811889f`, and `a1da0764cb66` are standalone UI, settings, random generation, printer management, scanner interaction or data-viewing code. They do not themselves implement a hostile collection or delivery flow.

## Dual-use and inconclusive

The following remain inconclusive unless marked dual-use; Hopper's purgatory target records both outcomes.

- `6a9535d9882b`, `5accf2da0fcf`: UI sends a request to an external handler; the receiving implementation and actual source of data are absent.
- `9d6639eea768`: hidden extraction and launch depend on an absent archive and companion executables.
- `57b045510425`: repeatedly closes browser windows whose titles match an argument; dual-use browser control with no target supplied.
- `8cc9f54a7de4`: remote desktop UI sends hide/show commands to a missing handler; dual-use.
- `6056329246bf`: launches externally supplied Python files and terminates selected Python parent processes; downstream scripts are absent.
- `255aa02d9777`: code transformation and identifier obfuscation utility; dual-use without a concrete hostile payload.
- `ccbf23acc9d3`, `410cfc8fffca`, `b391f1662d1d`, `6d25bce84ce7`: encrypted SDK archives contain minified browser network interception and cryptographic proof bundles. The manifests expose `postinstall1`, not npm's `postinstall` lifecycle, and the referenced script is absent; full bundled behavior and dependencies remain unverified. The fourth archive includes large binary proof resources.
- `7897d212eaa8`: 95 MB executable/archive; cleave timed out and atomscan scanned 2,218 entries without a hostile finding, leaving incomplete coverage.
- `1497a13739e3`: displays a false disk-loss threat and creates a shortcut to exit DOS; its visible actions do not establish the claimed damage, but the coercive presentation warrants further assessment.

