# Swift filetype mislabeled-bad review — 2026-11-04

The snapshot contains 40 files: 38 bad, 1 good and 1 inconclusive.

`ebb80190fdce` decodes and executes only `echo hello`. It is good, despite two original hostile findings. Both scanners now clear the hostile findings for this single-decoder benign command. The existing hostile fixture was corrected to encode a command that posts `/etc/passwd` to an example endpoint; both scanners retain both hostile findings on that host-data-transmission PoC.

`0f687522b60c` downloads a hidden executable, changes its permissions and runs it; `2cac47a02298` bridges an interactive shell over a TCP connection; `3f401db63ef1` repeatedly initiates calls to enumerated contacts. These are bad and both scanners already report hostile findings.

`fdacbb272964` copies credential-related host files to a hidden staging directory, sends beacon requests and performs CPU and disk degradation. It is bad; both scanners report a hostile finding. The beacon sends fixed status labels, not the staged files, so host-data exfiltration is not asserted.

`75f6da5ca0d0` is a Swift entry point that instantiates and starts a keylogger and runs its event loop. It is bad as a dedicated launcher; both scanners already identify the keylogger startup. Its capture implementation is external to this file.

`0d417f26cd8d` reads account and SSH-related files and constructs an HTTP POST containing the collected data. `2273c0d24985` combines subnet scanning and executable-delivery code with a socket report containing host details. `9d9d656c9ddb` constructs and sends a host fingerprint and implements socket-driven shell command dispatch. These PoC sources are bad, including where their sample endpoints or language errors may limit execution. Both scanners match new hostile findings combining the relevant collection/transmission or command-dispatch facts. Controls changing a shadow path, report marker, or command marker clear the corresponding new finding; other independent findings may remain. The findings are static correlations, not proof of successful network transmission.

The following 29 artifacts are bad based on the implemented attack, persistence, collection, or exfiltration code. Both scanners already report hostile findings; the principal observed traits are listed below. These source-level correlations do not establish successful compilation or execution.

- `1ea630d326a7`: Swift disk fill loop; Forks, fills disk, and connects.
- `3ad29f3a13f2`: Uploads shadow and SSH secrets; Deletes personal folders and key directories.
- `8d3b0ae1f9b7`: FTP upload after reading account files; FTP upload with SSH hostkey off.
- `4ccfb257d69a`: Boot script backgrounds a hidden file.
- `3298cb14ce26`: Records mapped HID keystrokes in a file.
- `e890c6253cae`: Loads a kernel module then setuid; Posts process list and SSH key.
- `0e0a7ae43f05`: Swift exfils cloud credentials over HTTP; Uploads harvested cloud files.
- `f536ce41f2c6`: Swift trojanized ls wrapper; Root cron launches remote shell.
- `0fd2dbd87537`: Swift botnet beaconing and command execution; Swift script installing a cron job.
- `ac50b0f1b189`: XOR file replacement with ransom notice.
- `a0e57f77e380`: Swift exfils cloud credentials over HTTP; Reads kube config and messages endpoint.
- `b1922160f730`: Swift network info HTTP exfil; Posts OS release and netstat.
- `db730c8488c8`: Swift logs HID device events alongside keystrokes; Swift HID keyboard input monitor.
- `da984cc890c6`: Swift Solaris file hiding; Swift script installing a cron job.
- `bb7196cf7408`: Swift SSH key file harvest; Swift Startup LNK dropper.
- `9b41d756bcdc`: Swift custom cryptominer; Miner persists through a hidden cron.
- `4ebf8f73dfa9`: Swift NetScaler HTTP tasking; Sweeps developer and cloud credentials.
- `1719a828ba33`: Swift iOS setuid shell privesc; Setuid shell on a jailbroken device.
- `55c37eda8155`: Dev-tcp stage chmodded and nohupped; Swift SSH credential HTTP exfil.
- `8b248511ad64`: Swift iOS setuid shell privesc.
- `6630d553a060`: Wraps both apt and the linker; Swift trojanized system utilities.
- `77bca9fffce0`: Swift Chrome login theft; Swift Apple ID phishing server.
- `f6a570a04abd`: Swift evals a base64-decoded string in a shell; Cats passwd into an HTTP client.
- `7a17083f7b36`: Log wipe paired with an exfil URL; Posts OS release and account paths.
- `57c7279eddf6`: Swift credential phishing lure; Swift SSH credential HTTP exfil.
- `dbbf34ab2cfa`: Swift SSH credential HTTP exfil.
- `1a1d77ecab45`: Curl posts SSH keys to an exfil URL; Preload hijack exfiltrates SSH keys.
- `2f517b4b1765`: Preload hook reads accounts and SSH; Preload cron posts to messages.
- `9e60b744bed5`: SSH hostkey off during release recon.

`549b16b7d5af` is a large OpenClaw source archive, not Swift source. Its tests construct runnable JavaScript payloads that execute a remote `curl | bash` command; it is bad under the embedded-PoC policy. A separate external-content test passes attack text to a defensive boundary and checks that it remains untrusted; that inert test no longer receives the unrestricted-persona hostile finding. The archive still retains the independent remote-shell payload findings.

`bf4621d5c545` is a Go module archive with 2,161 entries, including 332 shell scripts and more than 1,000 Markdown files. Both initial scanners reported no hostile traits; targeted searches found installer command examples and documentation, but the static review could not determine whether the remaining installer and integration scripts perform additional harmful actions through their dependencies. That specific analysis limit leaves it inconclusive; Hopper records the ruling through the purgatory compatibility target.

The archive review also corrected two misleading matches: an iMessage effect identifier is not the MobileSMS bundle ID, and “output system prompt template” is documentation about a template rather than a disclosure request. A wakeup-hook installer retains one suspicious dotfile-execution finding because it installs and makes a hidden hook executable.
