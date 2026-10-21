# Stranded member review, 2026-10-21

Reviewed the 75 explicitly queued extracted members individually. All 75 are
MALICIOUS payloads or operational offensive components. The three enclosing
archives retain their supplied convictions and were not re-judged.

These are static artifact judgments, not findings that any particular machine
was compromised. Kali/Empire, DAVTest and SecLists provenance supports legitimate
security assessment use; none of the supplied deployment context establishes an
actual intrusion or an authorized exercise. The decisions below rest on each
member's implemented effects: credential harvesting, covert control, exploitation,
privilege abuse, resource exhaustion, or extraction-root escape and defacement.
The native root-shell snippets require existing privilege, capabilities or a
setuid installation; calling setuid(0) does not itself defeat the kernel.

## Method and material distinctions

- Verified each listed member's SHA-256 before writing its one-line marker.
  The Debian extraction directories contain `usr/` directly; `data/usr` aliases
  preserve the member paths specified by the queue without changing sample bytes.
- Ran atomscan and cleave facts on all 75 members, saved results, inspected source
  control flow and relevant calls, then re-ran atomscan on all 75 after edits.
  Final scans disabled updates and reference fetching. Tool scores were not used
  to establish behavior or verdicts.
- Decoded embedded Base64 PE files, GZip/Deflate assemblies and UTF-16 examples
  without executing them. Disassembled .NET method bodies with dnfile/dncil,
  and inspected relevant native code and call sites with Rizin.
- WireTap dispatches surveillance commands into audio recording, keyboard-hook
  logging, clipboard traces, screenshots and webcam capture. SharpChromium reads
  login/cookie databases, unwraps the Local State key with DPAPI and decrypts
  browser blobs. USBKeystrokes' embedded assembly filters USB ETW payloads,
  maps HID keys and queues recorded input for the script's window attribution.
- SweetPotato's managed entry selects impersonation exploits, duplicates the
  intercepted token and launches the requested process. SpoolSample calls an
  embedded native `DoStuff` export whose printer-RPC calls use the target and
  capture-server arguments. PrintNightmare's native code calls NetUserAdd and
  NetLocalGroupAddMembers (at RVAs 0x1956 and 0x197d); its exported `test`
  function alone is not the account-creation behavior. PrintDemon's DLL starts
  PowerShell through CreateProcessW at RVA 0x1ebc, with socket handling around it.
- Both Mimikatz copies are working reflective loaders with different embedded
  payload hashes, not inert test mocks. ChromeDump's embedded System.Data.SQLite
  libraries are legitimate dependencies; the surrounding script's credential
  database queries and plaintext export establish the wrapper's purpose.
- Laudanum PHP enforces an IP allowlist and session authentication; its ASP page
  has an IP gate. Those restrictions limit who can invoke the implemented web
  shells. The WordPress template instead uses `if(true)` around command dispatch
  and `if(false)` around the login UI. The separate WordPress plugin has a broken
  reverse-shell branch involving an undefined `$ip`; its reachable request-command
  path and chmod/chattr self-protection establish the verdict without claiming a
  working reverse connection.
- Inspected WAR entries and their JSP request-to-Runtime.exec path. Inspected ZIP
  central/local headers and small stored bodies without extracting traversal
  paths or expanding the bomb. Every depth archive contains `../` repeated by
  its depth, followed by `index.php`, whose stored bytes are `hacked\n`. The bomb
  has 190,023 entries with overlapping compressed extents and declares
  4,507,981,427,706,459 bytes of output.

## Trait changes and checks

Added a raw NTLM hash-replay composite in the existing pass-the-hash/ntlm home.
It requires the hash declaration, slicing into the NTLM-named buffer, assignment
of that buffer as the HMAC key, the HMAC-MD5 constructor, and an already-admitted
SMB command executor. The neutral facts remain notable in declaration,
authentication and cryptographic homes. No sample digest, filename or enclosing archive
conviction gates the new rule.

SCM create/delete packet traits now require assignment from a builder invocation,
rather than merely a matching function declaration. PowerBreach descriptions no
longer assert durable persistence or a proven relation between an arbitrary loop
and evaluation. The native browser composite describes co-occurrence rather than
a proved collection chain and maps to browser credential acquisition, not LSASS
dumping.

Five mutation/precision controls passed: renamed sample filename; password-derived
hash instead of raw hash input; raw-hash client with service operations removed;
unrelated MAC key; and builder declarations with no calls. The first retains the
new replay finding; the remaining four exclude it. Creation/deletion findings
also remain absent for declarations alone. Reproduce with `run-controls.py`
and the queued Invoke-SMBExec.ps1 path as its argument.

All non-traversal members retain at least two hostile findings. Each traversal
member retains one supported hostile defacement finding and one engine-emitted
suspicious path-traversal finding. There is one implemented attack outcome here;
no duplicate hostile label was invented just to meet a numerical target.

The markers contain the following exact lines (each <=72 characters). Complete
scan/facts output, decoded artifacts, IL/native inspection and control results are
in the task scratch directory `stranded-review/`.

## Individual decisions

| Member | SHA-256 prefix | Marker line |
|---|---|---|
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/collection/Invoke-WireTap.ps1` | `8e2d912895a1` | WireTap: embedded payload records keys, audio, screen and camera |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/credentials/Invoke-Mimikatz.ps1` | `cd29dfe9a817` | Mimikatz: logon/private-key dumper; clarify browser trait |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Invoke-BypassUAC.ps1` | `e84bd927b3b7` | BypassUAC: injects DLL elevator and self-deleting payload launcher |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/credentials/Invoke-DCSync.ps1` | `65671d00aad1` | DCSync: reflectively runs replication abuse and extracts NTLM hashes |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/persistence/PowerBreach.ps1` | `46b36e5b7147` | PowerBreach: triggerable remote-code backdoor; clarify traits |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Invoke-SweetPotato.ps1` | `7d847be9fa5a` | SweetPotato: embedded token impersonation exploit launches a process |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/credentials/Invoke-SharpSecDump.ps1` | `585ea93278bc` | SharpSecDump: remote SAM and SECURITY hive credential recovery |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Invoke-MS16032.ps1` | `14e3928a82cf` | MS16-032: races leaked thread tokens to launch a SYSTEM command |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/management/Invoke-Vnc.ps1` | `f9413b36bded` | Invoke-Vnc: reflective VNC implant provides bind or reverse control |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/code_execution/Invoke-MetasploitPayload.ps1` | `2a6208d649f5` | MetasploitPayload: hidden remote-code cradle disables TLS checks |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/PowerUp.ps1` | `19a5148af319` | PowerUp: service-command abuse and bulk saved-password extraction |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/credentials/dumpCredStore.ps1` | `faefdb1a1aea` | dumpCredStore: enumerates and prints Credential Manager secrets |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/collection/Invoke-NetRipper.ps1` | `77347b2a804c` | NetRipper: injects plaintext TLS capture with credential filtering |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/credentials/Invoke-CredentialInjection.ps1` | `6bbbc6268b6d` | CredentialInjection: injects Winlogon to create credential logons |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Invoke-EventVwrBypass.ps1` | `47828613e6a7` | EventVwrBypass: hijacks elevated command association then cleans up |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Invoke-Printnightmare.ps1` | `6640b2832e51` | PrintNightmare: printer DLL exploit installs local admin account |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Invoke-PrintDemon.ps1` | `11e35e816755` | PrintDemon: printer DLL overwrite, SYSTEM shell and Run-key launcher |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/exploitation/Invoke-SpoolSample.ps1` | `713d4d7b3695` | SpoolSample: embedded printer RPC coerces remote authentication |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/lateral_movement/Invoke-InveighRelay.ps1` | `d846056c60f7` | InveighRelay: relays captured NTLM to SMB commands; require SCM calls |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Get-System.ps1` | `cfbfd03393d7` | Get-System: steals SYSTEM tokens or impersonates service pipe client |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/credentials/Invoke-PowerDump.ps1` | `5247c55a12a9` | PowerDump: impersonates LSASS and decrypts SAM password hashes |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/collection/Get-SharpChromium.ps1` | `370651164347` | SharpChromium: decrypts browser passwords and exports session cookies |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/credentials/Invoke-SessionGopher.ps1` | `fb1752ab4f15` | SessionGopher: sweeps saved remote sessions and recovers passwords |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/persistence/Invoke-RIDHijacking.ps1` | `00ca4323c1dc` | RIDHijacking: rewrites SAM identity RID to impersonate admin account |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/lateral_movement/Invoke-PsExec.ps1` | `7bd10eb7ad6d` | Invoke-PsExec: runs remote commands through temporary SYSTEM service |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Invoke-SDCLTBypass.ps1` | `e48b5c4b4998` | SDCLTBypass: hijacks elevated runas command and removes override |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Invoke-FodHelperBypass.ps1` | `737cbc10410d` | FodHelperBypass: DelegateExecute hijack launches hidden encoded code |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Invoke-EnvBypass.ps1` | `1f1a33a353b2` | EnvBypass: windir hijack makes SilentCleanup run hidden code |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/collection/Invoke-SharpLoginPrompt.ps1` | `b6e3c420332f` | SharpLoginPrompt: fake credential prompt prints and validates secrets |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/exploitation/Exploit-Jenkins.ps1` | `0082e77d1f53` | Jenkins exploit: posts Groovy process commands and harvests results |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/collection/Get-Keystrokes.ps1` | `73eff2e8bfdd` | Get-Keystrokes: records translated keys with foreground window titles |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/exploitation/Exploit-JBoss.ps1` | `34b897daef0e` | JBoss exploit: abuses JMX deployment and triggers supplied WAR code |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Invoke-Tater.ps1` | `aefe5bda0b8c` | Tater: poisons NBNS and reflects NTLM to local SMB command execution |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/persistence/Persistence.psm1` | `bfbf003f2b4a` | Persistence: conceals profile payload with WMI, task and Run triggers |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/credentials/Invoke-NTLMExtract.ps1` | `8e919f6f27cf` | NTLMExtract: impersonates Winlogon and decrypts SAM password hashes |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/lateral_movement/Invoke-SMBExec.ps1` | `34204bf85370` | SMBExec: raw hash replay and remote service commands; add hash trait |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Get-GPPPassword.ps1` | `0394a74e6ccc` | GPPPassword: sweeps SYSVOL and decrypts stored policy passwords |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/credentials/DomainPasswordSpray.ps1` | `d456f59b2de2` | DomainPasswordSpray: bulk LDAP guessing avoids account lockout |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/collection/Get-ChromeDump.ps1` | `c169b851c5bb` | ChromeDump: queries login database and exports DPAPI-decrypted secrets |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/collection/Invoke-Inveigh.ps1` | `d0cc2a0dff61` | Inveigh: name-service spoofing and NTLM credential interception |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/collection/Invoke-CredentialPhisher.ps1` | `8790ceefd3db` | CredentialPhisher: deceptive login dialog harvests validated passwords |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/collection/Get-USBKeystrokes.ps1` | `39d876d3787e` | USBKeystrokes: decodes USB ETW events and records keys by window |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Invoke-BypassUACTokenManipulation.ps1` | `43b27e7affe2` | UAC token bypass: alters token integrity and impersonates elevation |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Invoke-MS16135.ps1` | `10bf23c56e3d` | MS16-135: corrupts win32k bitmap pointers to copy the SYSTEM token |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/credentials/Invoke-TokenManipulation.ps1` | `65086354b86c` | TokenManipulation: steals privileged tokens and spawns as their users |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/lateral_movement/Invoke-ExecuteMSBuild.ps1` | `d45b9c76ff26` | ExecuteMSBuild: runs encoded PowerShell via inline MSBuild task/WMI |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/collection/Get-FoxDump.ps1` | `f2bf815e9a84` | FoxDump: decrypts Firefox login secrets with NSS and stages plaintext |
| `7681be/data/usr/share/powershell-empire/empire/server/data/module_source/privesc/Get-SiteListPassword.ps1` | `28f9f645e43c` | SiteListPassword: sweeps and decrypts saved McAfee server credentials |
| `7681be/data/usr/share/powershell-empire/empire/test/data/module_source/credentials/Invoke-Mimikatz.ps1` | `b0f8ae32dd20` | Test Mimikatz: working logon/private-key dumper; clarify browser trait |
| `7681be/data/usr/share/powershell-empire/empire/server/data/agent/agent.ps1` | `d14c308e0b24` | Empire PS agent: remote task execution and chunked file exfiltration |
| `7681be/data/usr/share/powershell-empire/empire/server/data/agent/ironpython_agent.py` | `3b05a309d6c4` | IronPython agent: remote code tasking and chunked file exfiltration |
| `7681be/data/usr/share/powershell-empire/empire/server/data/agent/agent.py` | `3a3f6dd119c2` | Empire Python agent: remote shell/code tasking and file exfiltration |
| `7681be/data/usr/share/powershell-empire/empire/server/data/misc/windows.c` | `f29d59be3acc` | Empire C stager: downloads unchecked code and executes RWX fiber |
| `6c25e8/data/usr/share/davtest/backdoors/asp_cmd.asp` | `c4af7a5b8548` | CmdASP: HTTP form commands run through WScript.Shell with output |
| `6c25e8/data/usr/share/davtest/backdoors/php_backdoor.php` | `61cf34663bc9` | PHP backdoor: request-driven commands, file access and database shell |
| `6c25e8/data/usr/share/davtest/backdoors/perl_cmd.pl` | `98278a99ae79` | Perl CGI backdoor: query string runs as a shell command with output |
| `8fa887/SecLists-2025.3/Web-Shells/laudanum-1.0/php/shell.php` | `4806ec0046ce` | Laudanum PHP: authenticated command webshell disguises access denial |
| `8fa887/SecLists-2025.3/Web-Shells/laudanum-1.0/asp/shell.asp` | `ae6163481f57` | Laudanum ASP: IP-gated command webshell hides behind HTTP 404 |
| `8fa887/SecLists-2025.3/Web-Shells/laudanum-1.0/wordpress/templates/shell.php` | `0291cccda354` | Laudanum WP template: command webshell disables session auth gate |
| `8fa887/SecLists-2025.3/Web-Shells/WordPress/plugin-shell.php` | `8933b5c6ad4d` | WP shell: request commands and self-protection with chmod/chattr |
| `8fa887/SecLists-2025.3/Web-Shells/laudanum-1.0/jsp/cmd.war` | `d4b46713dbd4` | Laudanum WAR: bundled JSP directly executes HTTP command parameters |
| `8fa887/SecLists-2025.3/Payloads/Zip-Bombs/zbxl.zip` | `eafd8f574ea7` | zbxl: overlapping ZIP streams declare 4.5 PB of expansion for DoS |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-01.zip` | `14d823c36474` | Zip traversal 01: escapes extraction root to overwrite index.php |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-02.zip` | `2e37907e4999` | Zip traversal 02: escapes extraction root to overwrite index.php |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-03.zip` | `34dc22d9a5f2` | Zip traversal 03: escapes extraction root to overwrite index.php |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-04.zip` | `1966ac5964c2` | Zip traversal 04: escapes extraction root to overwrite index.php |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-05.zip` | `940187e30e17` | Zip traversal 05: escapes extraction root to overwrite index.php |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-06.zip` | `3fd5ebc586cb` | Zip traversal 06: escapes extraction root to overwrite index.php |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-07.zip` | `87c252752eac` | Zip traversal 07: escapes extraction root to overwrite index.php |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-08.zip` | `5a7a1c6081ed` | Zip traversal 08: escapes extraction root to overwrite index.php |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-09.zip` | `3dc7b8fbf340` | Zip traversal 09: escapes extraction root to overwrite index.php |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-10.zip` | `5f4770219d1b` | Zip traversal 10: escapes extraction root to overwrite index.php |
| `8fa887/SecLists-2025.3/Miscellaneous/Source-Code/c-linux/tiny-shell.c` | `b96a67e3d43a` | tiny-shell C: unguarded root UID request followed by unrestricted sh |
| `8fa887/SecLists-2025.3/Miscellaneous/Source-Code/c-linux/root-shell.c` | `9f9cc2950dbd` | root-shell C: root UID/GID shell helper intended for setuid install |
| `8fa887/SecLists-2025.3/Miscellaneous/Source-Code/c-linux/root-shell2.c` | `2b9156890423` | root-shell2 C: unguarded root UID request then unrestricted bash |
