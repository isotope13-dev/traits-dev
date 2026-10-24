# Stranded Android members, 2026-10-24

The four requested members were examined statically. No specimen or fixture was executed.
The three enclosing archive convictions were preserved.

## Identifications and decisions

- **Installer (8202c388…): MALICIOUS.** A universal C++ Mach-O launcher. The ARM64 entry point at `0x100000690` builds a string and invokes `system` at `0x1000006b8`. Its decryptor XORs 37,077 bytes using a state initialized to `0x11667`; each byte advances the state as `((state * 0x3785) & 0xffffffff) % 35999`. The modulus is derived from the embedded `09:59:59` string. Independent decoding exactly reproduced Cleave's recovered command. The command runs an obfuscated AppleScript with password phishing and `dscl` validation, browser/wallet/Keychain/Notes/document collection, ZIP upload, cleanup, Ledger Live replacement, and a downloaded command installed through a system LaunchDaemon. The password is cached and reused with `sudo -S`. The upload precedes cleanup; wallet replacement and persistence follow it. No final downloaded payload or successful TCC bypass is assumed.
- **DAVTest perl_cmd.pl (98278a99…): MALICIOUS.** The complete 580-byte CGI reads `QUERY_STRING`, decodes percent spaces and semicolons, passes the same scalar to backticks, and prints the captured lines in its HTTP response. There is no authentication gate. Kali/DAVTest packaging explains its legitimate testing use: the bundled README documents optional backdoor upload, and DAVTest sends it only when requested. The label describes this member's deployable backdoor role, without claiming unauthorized deployment. It has only command execution and returned output as attack functions; decoding and formatting do not justify inventing a third hostile behavior.
- **Android Frida agent.py (fdcd56c6…): BENIGN.** An explicit CLI assessment tool. It lists packages/components, checks readable storage, captures traffic with tcpdump and ADB pull, and spawns/attaches a caller-selected app to install Frida certificate/hostname verification hooks. Results are returned locally. Its `ssl` operation actually replaces verification behavior; it is not merely passive detection. No remote task source or collection upload is configured.
- **Android process.py (c60603ee…): BENIGN.** A caller-targeted Android assessment orchestrator using ADB, Frida and Objection. It enumerates components, disables root checks and TLS pinning, checks debug settings, searches process memory for secret-like strings, lists Keystore entries, and writes a local JSON report. It does not implement a remote command channel. The root-check bypass remains suspicious despite the benign tool verdict. Tool output heuristics are not proof that a bypass succeeded; Keystore listing is not private-key export.

The wheel recovered with `forager fetch --all-wheels pkg:pypi/ai-forge-cli@2.1.6`
exactly matches SHA-256 `754533af96b223512d45d89d63ade1cb302fef4b9cb2145dab0bfc3e1ac8eb4e`.
Recovered artifacts and `.forage.json` provenance remain in the named scratch tree.
Neither member verdict depends on the archive's conviction or VirusTotal count.
Actual deployment authorization is unavailable for every member.

## Rule corrections

The old shell-task text matcher accepted `cmd = ["adb", "shell", ...]` and promoted it into suspicious remote tasking near a subprocess call. It established neither a dispatch branch nor a remote task source. Shell selection is now a neutral branch observation requiring comparison/case syntax or a structured command-field selector; Rust/C# arrow arms are also retained. The nearby-process-call observation is notable and explicitly describes proximity. C2 consumers still require their independent HTTP task protocol and file-task evidence. Exact consumers were updated; no bare ancestor-directory consumers select the relocated groups.

Frida USB device lookup moved from attestation evasion to instrumentation and no longer claims attachment. Its capability is preserved for legitimate callers; the attestation-relay composite still references it. Existing Java instrumentation atoms also cover Python controllers' embedded JavaScript. `Java.perform` is described as a callback API, not attachment.

A subprocess `-U` flag does not universally mean package upgrade: Frida uses it to select USB. The neutral option remains visible. The pip upgrade observation now binds pip, install and the upgrade flag to the same subprocess argument list, preserving short `-U` upgrades while rejecting an unrelated Frida call elsewhere in the file.

New notable observations cover Objection TLS-pinning disabling, memory search, Keystore listing and a Frida SSLSession verifier replacement returning true. Explicit Objection root-check disabling is suspicious. Literal matching excludes Python docstrings. The memory-search matcher uses its fixed command prefix because Atomscan's embedded parser splits interpolated literals; Cleave facts preserve the reconstructed f-string.

## Verification

`check.py` consumes an Atomscan JSONL report and checks `cases.json`; it never imports or executes fixtures. Controls cover actual dispatch versus ADB argv, pip short upgrades versus USB selection, unrelated pip/Frida calls, executable command literals versus docstrings, forwarding versus permissive verifier hooks, Rust match arms, and retained hostile attestation-relay detection. The existing mesh HTTP tasking suite covers Python/Go attack fixtures outside this batch, benign monitoring, quoted documentation, variable renaming and endpoint changes.

The initial cached Installer report contained extra redundant neutral aliases. Fresh original-rule and edited-rule scans agree on its capabilities and hostile/suspicious counts. Architecture-specific XOR observations may select different universal-binary slices; both decode the same command. All hostile Installer and Perl detections are retained. The removed Android subprocess-launch umbrella is a bare OR wrapper: its underlying `run-ast`/`check-output-ast` detections remain. The wrapper ceases to surface when the false tasking composite no longer cites it; this is not lost process-execution coverage.

Archive-member comparison found the same false remote-tasking claim on three additional scripts: conducting-mobile-app-penetration-test, exploiting-deeplink-vulnerabilities, and testing-android-intents-for-vulnerabilities. Their complete source was inspected. Each constructs ADB `shell` argv for app/storage/intent testing rather than dispatching controller-supplied shell tasks. Their underlying execution and network detections remain. All three archive parents retain their hostile and suspicious totals: Installer 7/8, DAVTest 19/7, wheel 3/35. In the wheel's union of findings, the removed tasking ID is replaced by the supported root-check bypass ID; unchanged totals do not conceal that semantic correction. The complete per-member and archive comparison, including classifier output and changed findings, is in `review.json`.

The installed model reports feature spec 18 while the current engine expects 21; newer features are absent from the classifier until it is retrained. Static findings remain independently reviewable. The four assessed member classifier verdicts agree with the individual judgments. The wheel's own `az/whl` classifier route remains benign (`0.6462087`), while member aggregation yields `0.99`, level 25. Its confirmed archive conviction is not changed by that disagreement. The Installer archive and DAVTest classify at level 0 before and after; both assessed Python members remain at level -1.

Marker lines (also prepared verbatim for the commit body):

```text
Installer stealer: phishes passwords, uploads stores, adds launchd
DAVTest CGI: unauthenticated query commands and returned output
Android Frida agent: local assessment; fix tasking FP, add hooks
Android analyzer: local audit; retain root bypass, add memory reads
```

Fresh scan hostile/suspicious counts:

| Member | Judgment | Before | After |
|---|---|---|---|
| Installer | MALICIOUS | 7 / 7 | 7 / 7 |
| perl_cmd.pl | MALICIOUS | 2 / 1 | 2 / 1 |
| Android agent.py | BENIGN | 0 / 1 | 0 / 0 |
| Android process.py | BENIGN | 0 / 1 | 0 / 1 |

The process.py suspicious ID changes from false remote tasking to supported root-check disabling. No hostile finding was lost in any member of the three archives.

The full validator's two mesh-fixture suspicious minima were updated from two to one after relocating the neutral shell-selector/process-call observation. Both hostile minima and minimum scores are unchanged. Each fixture now explicitly requires the relocated notable observation, preserving its capability coverage as well as the existing hostile protocol requirements.
