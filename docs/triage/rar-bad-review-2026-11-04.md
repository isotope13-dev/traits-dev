# RAR mislabeled-bad review — 2026-11-04

The 40 archives were reviewed: 19 bad, two good, and 19 inconclusive.

`d60cd43aa65c` contains only an HTML 404 error page, despite its web-shell filename. Hopper moved it to good. `5116b10302d1` contains a PHP web shell that executes a request parameter and is bad; both scanners already flag it.

`5bde055523d3` contains an image whose archive member name embeds a Base64-decoding shell command substitution that fetches and runs a remote script. It is bad; the command requires an unsafe shell interpretation of the name to execute. A new finding combines encoded-command and decoder-to-shell evidence from the RAR member metadata. Both scanners flag the original; a valid RAR with the decoder option changed clears the control. Full validation passed.

`191b7d804e65` expands to an obfuscated ActiveX script whose 23 KB of code is followed by about 101 MB of NUL bytes. The padding causes the source parser to skip it. This is hostile obfuscation; the payload's full behavior remains unconfirmed. A new finding combines the NUL distribution, parser guard, oversized source and computed ActiveX indicators. Both scanners flag the script and archive; replacing the ActiveX identifier clears the control.

`68314e93b47d` contains an HTA that reconstructs and runs a remote `mshta` command from string fragments. It is bad. A new finding matches the recovered HTA and containing archive in both scanners, while changing the command fragment clears the control. The previous generic hostile finding for a small compressed RAR containing an HTA was downgraded to suspicious: those archive properties alone do not establish hostile behavior.

`95262c4094a9`, `adf6e9d35526`, `f013b00c7095`, `278bc812d9cd`, `9a3f15daaafd`, `ef865dc51fc9`, `853ce6e1ed15`, `cef405879cfd`, `2e79f462f9c8`, `2122774f22c2`, and `a6e1abc4f0be` contain alternate-stream paths that traverse into the Windows Startup folder and carry HTA, VBS or executable payloads. All are bad; existing findings identify the traversal.

Full validation passed after these changes.

`c16be243e6de` carries multiple alternate-stream traversal paths targeting Startup shortcuts. `9cbbaafb4a27` contains an accessible XWorm client with remote tasking, keylogging and screenshot functionality. Both are bad and existing findings identify them.

`3fbdc5c4ace9` and `4b38723087c6` contain unsigned, high-entropy-code executables with approximately 452 MB and 770 MB of zero overlay, respectively. They are bad as hostile obfuscation; this does not establish the exact payload behavior. A new finding combines the dominant, near-zero-entropy overlay, its size, code entropy and unsigned status. Both scanners flag each extracted executable, while removing the overlay from the first clears the control. The encrypted nested archive around the first executable must be opened separately to expose it.

`5d613b653d2f` contains a Chrome APK. Its v2 and v3 signatures verified with `apksigtool`; the certificate fingerprint matches the [Google first-party signing key documented in Android source](https://android.googlesource.com/platform/frameworks/support/+/7be3a623dfcf461ff6e2004799ac2e652c8d23a8). Hopper moved the archive to good.

The following archives remain inconclusive because their encrypted members could not be reviewed with the tested common passwords: `f67ef1e55364`, `03046b31cfc9`, `c859a8ec2353`, `ec963919f66e`, `fc5da4c7e277`, `5965e9a181aa`, `df1a763ffa0f`, `b6abf8a3d5e8`, `7e69dbb24d94`, `7487c3948167`, `4236de234516`, `874405de122d`, `308698e41de4`, `7b90b1c5ff11`, `2ae69fc0aa76`. The accessible program in `7b90b1c5ff11` is VMProtect-packed and requests elevation, but those facts do not establish malicious behavior; the generic finding was downgraded to suspicious.

`7faa538f84e7`, `8df0882f55a1`, and `123ce26ce35e` contain disk images with .NET executables. Their names and obfuscated or dynamic-loading code are insufficient to establish the executables' full behavior; they remain inconclusive.

`79a250df5882` contains a nested archive whose supplied password exposed an installer bundle, including 17 executable or DLL components and opaque data files. Neither scanner reported a hostile finding on those components, but the data and bundle behavior remain unverified; Hopper records it as inconclusive.
