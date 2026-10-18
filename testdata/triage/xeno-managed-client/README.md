# Xeno managed client triage

Sample: `xeno rat client.exe`, 47,616 bytes.

SHA-256: `d6603decfbf5825b9f6f246c7b4c4a4149ff57ed8ce789fceb46d5e8c9ced9b4`

Assessment: **hostile**. This is a managed remote-access implant with remotely
supplied plugin execution and victim monitoring. Its present configuration
appears broken; operational readiness and malware capability are separate facts.

Hopper accepted the final scan. The sample was already in the bad pool:
relabeling returned one no-op, zero absent samples, and zero failures.

## Reconstruction

Mono disassembly and ILSpy project decompilation recovered the complete client
without executing it. The PE targets .NET Framework 4.8 and contains no managed
resource payloads or bundled plugins. The following behavior was traced through
the recovered methods and their async state machines.

| Component | Evidence and behavior |
| --- | --- |
| `Program.Main` | Redirects console output into an internal log, registers an unhandled-exception restart handler, checks administrator status, takes a named mutex, waits one second, and cycles controller entries with a ten-second retry delay. |
| Relocation and startup | Relocation is conditional on `Install_path != "nothingset"`; the supplied build leaves that sentinel unchanged. Startup registration is conditional on `DoStartup == 1`; its value is **2222**, so that entry-point branch is disabled. |
| Controller configuration | Nine strings of the form `http://<domain>/loader.ps1` are passed directly as the hostname argument to `SocketTaskExtensions.ConnectAsync`, on TCP port **1234**. There is no HTTP fetch or URL normalization in that path. Normal hostname resolution is therefore likely to fail. |
| `Node.AuthenticateAsync` | Echoes a server challenge, checks the seven-byte marker `moom825`, exchanges node/socket type and ID, and authenticates additional sockets to the main peer. |
| `Handler.Type0Receive` | Receives control opcodes: open subchannel, send machine information, terminate, restart, and uninstall. The self-restart handler also relaunches the entry assembly and kills the current process. |
| `Handler.Type1Receive` | Implements a heartbeat subchannel with a receive timeout and one-byte reply/failure messages. |
| `Handler.Type2Receive` | Handles update requests, plugin dispatch, node IDs, disconnect, and diagnostic commands. Diagnostics can enumerate/remove cached plugins and return the internal process log. |
| `DllHandler.DllNodeHandler` | Receives a plugin name, requests missing bytes, calls `Assembly.Load(byte[])`, caches the assembly, instantiates `Plugin.Main`, and reflectively invokes its public `Run` method with the live node. The receive-to-load relationship is visible in the decompilation. The PE trait itself reports the relevant capability combination rather than claiming to reconstruct this data flow. |
| `Handler.GetAndSendInfo` | Sends a machine fingerprint, account names, client version **1.8.7**, Windows version/architecture, antivirus product names, and admin status to the controller. |
| `Handler.SendUpdateInfo` | Sends active foreground-window process/title and idle seconds. Window APIs are queried through P/Invoke; idle duration comes from `GetLastInputInfo`. This core contains no keylogging or screenshot implementation. A later plugin could add capabilities, but none was supplied in this sample. |
| `Utils.AddToStartupNonAdmin` | Available routine writes a quoted executable path into HKCU's `Software\Microsoft\Windows\CurrentVersion\Run`. Disabled by the current entry-point configuration. |
| `Utils.AddToStartupAdmin` | Available routine writes logon-triggered task XML with `HighestAvailable`, parallel instances, and unlimited execution time, then imports it through a hidden `schtasks.exe /Create /TN ... /XML ... /F` process. Disabled by the current entry-point configuration. |
| `Utils.Uninstall` | Removes matching Run values/tasks, starts hidden `cmd.exe` with a Base64-decoded `/C choice /C Y /N /D Y /T 3 & Del "` prefix plus its own assembly path, then kills itself. This remains reachable through controller opcode 4 if a connection succeeds. |
| `Encryption`, `SocketHandler`, `Compression` | AES encryption/decryption uses the shipped key bytes `00` through `1f` and a zero IV. The framework defaults supply CBC and PKCS7. Frames use a four-byte length, packet-type bytes, and optional LZNT1 compression through `RtlCompressBuffer`/`RtlDecompressBuffer`. |

`RecvAllAsync_ddos_safer` and `RecvAllAsync_ddos_unsafer` are receive helpers;
their names do not establish DDoS behavior. No process injection, credential
stealing, browser collection, or camera/audio capture code was found in the
supplied core. These were not inferred from Xeno RAT's family reputation.

Configured controller strings, retained as static indicators rather than
contacted during analysis:

```text
http://qq88.com.mx/loader.ps1
http://qq88-n1.com/loader.ps1
http://qq88.fitness/loader.ps1
http://qq88z.com/loader.ps1
http://qq882fa.com/loader.ps1
http://hi88vip10.com/loader.ps1
http://qq88.forex/loader.ps1
http://qq88-t1.com/loader.ps1
http://csqq88.com/loader.ps1
```

## Detection changes

The original scan had two hostile findings: existing Xeno family recognition
and the third-party Xeno signature. The third-party signature's description
incorrectly said “Detects Blacksuit”; only that metadata description was fixed.
Its matching logic is unchanged.

New detection covers the combined managed network/plugin-dispatch,
foreground-window/idle monitoring, hidden process creation, and delayed
self-removal capability set. Every role is required; family strings, plugin
names, controller domains, mutexes, file names, and exact sizes are not.
The conjunction identifies a remote implant profile without claiming that
mere PE name-heap co-occurrence proves source-to-sink flow.

Separate suspicious observations cover logon-task creation code and Run-key
mutation references. Neutral observations cover compiled reflection members,
active-window title APIs, native compression, and the short `Aes` metadata name
with encrypt/decrypt transform references. `Aes` is too short for normal string
extraction, so its NUL-delimited name is matched within `.text` and combined with
the managed framework and crypto-transform evidence.

The repaired scan yields **three hostile and four suspicious findings**. It
does not claim the disabled startup routines run or treat the configured URLs
as executed PowerShell downloads.

## Verification

```sh
python3 testdata/triage/xeno-managed-client/check.py \
  --sample '/Users/t/Downloads/xeno rat client.exe'
```

The harness compiles `Probe.cs` as libraries and statically scans them; it never
loads or executes the resulting assemblies. Fifteen controls include the full
capability combination, removal of each required role, ordinary networking,
reflection-only plugins, local window inspection, standalone persistence,
AES, compression, and a plain library. The original sample is checked alongside
them. All passed.

Unrelated concurrent edits in the shared working tree failed general validation.
This triage's changes were copied onto repository base `9070a527b` in
`/tmp/triage/xeno-d6603d/validation` and validated separately with the same sibling
Cleave binary. Validation output is retained in `/tmp/xeno-isolated-validate.log`.
The final Hopper scan uses that same isolated ruleset.
`make validate` passed in that snapshot, including all benign, hostile,
reverse-shell, supply-chain, and other configured validation groups.

Session artifacts: complete disassembly in `/tmp/xeno.il`, decompiled project in
`/tmp/triage/xeno-d6603d/decompiled`, facts in `/tmp/xeno-facts.json`, and final
Atomscan report in `/tmp/xeno-final-atomscan.json`.
