# Registry-script mislabeled-bad review — 2026-11-04

The 24 files were reviewed: 10 bad, eight good, three dual-use, and three inconclusive.

`601742aace27` places a logoff command in a machine startup key, and `a2b900343185` declares deletion and replacement of the entire machine Run key. Both are bad. New findings combine the relevant registry targets and operations. Both scanners match the originals and controls with the relevant operation changed clear. The latter file contains repeated registry headers, so actual import behavior may depend on the parser.

`45bcf10882ee` disables the Avira scheduler service. That weakens scheduled protection but can also be an administrative action, so it is dual-use; the corresponding finding is suspicious. Both scanners matched it, and changing the service startup value cleared the control.

`7e4310d14a05` attempts to export an autostart key over registry files in a loop. Both scanners already flag the infection attempt. It is bad.

`15974537623e` is a registry/batch polyglot that copies itself to deceptive BAT filenames and contains commands to delete the Windows system tree. It is bad; a new finding combines those commands with the registry header, and both scanners match while a deletion-target control clears. The attempted commands are not proof they succeeded.

`a2ee9b3480d3` stores an encoded PE, endpoint list and PowerShell loader in registry values. The recovered script reads registry values, decodes and launches a DLL, and evaluates decoded commands. It is bad. Both scanners match a new finding on the carrier; changing the encoded registry-read operation clears the control. This is static evidence and does not prove successful network delivery.

Full validation passed after the latest findings.

`0eb814f0a18d` declares an empty Winlogon shell and forced logoff in Userinit. `47ddba2f3a93` declares an empty shell, disables Task Manager and registry editing, and displays a compromise notice. `4d12f530a00f` changes the EXE association to a text-file handler, disables registry editing and declares several startup scripts. All are bad. New combined findings match in both scanners, while controls changing the relevant logoff, notice or association clear them.

`74657116adba` deletes and replaces autostart keys, redirects browser settings and stages a silent registry import from a certificate-named file. The referenced file is absent, but the deletion and disguised import are explicit. `03a5b194f82a` declares desktop, logoff and recovery restrictions alongside a false Win.com disk-format notice. Both are bad; new findings match in both scanners and their respective controls clear. The latter notice contains embedded quotes that may affect import parsing.

The following are good based on their standalone contents: `87b97b36bba6` records activation settings; `5e22e12fc345` changes the clock format to an offensive message but has no execution or security-disabling behavior; `21b9d105be9d` and `eca56d0cdf09` set browser homepages; `f8402de15ec4` adds a Notepad context-menu action; `527e789f7574` is inert application configuration; `3a7a56cae09a` configures the Windows shared-access service; and `bb0a8dfdfa81` writes policy-looking values under an unrelated registry subtree.

`17d8558a2820` disables an old Word macro-protection setting and is dual-use. `c71677c6ecfa` changes and locks a browser homepage while disabling command and registry tools; those settings can also be used for managed configurations, and the referenced site's role was not established, so it is dual-use. `2c6efeaa9145`, `9b887aa1c435`, and `4a000b139252` reference absent executables whose behavior cannot be determined from the registry files; they are inconclusive. Hopper stores dual-use and inconclusive samples under its inconclusive compatibility target.
