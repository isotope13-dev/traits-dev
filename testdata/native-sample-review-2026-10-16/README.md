# Native sample review, 2026-10-16

Judgments use the submitted bytes and disassembly, independently of ML and
collector filenames. No sample was executed. No program-supplied executable,
account list or update payload was fetched. These are local PE specimens;
there are no fetched package dependencies to scan in isolation.

| SHA-256 | Identity | Judgment | Final unique hostile / suspicious traits |
| --- | --- | --- | --- |
| a6fac2ae71e1c6695cb49a163ba5958ea7f76550a7a9cdcc8ba2995253eb515e | NtHook installer with safemon surveillance DLL | MALICIOUS | 2 / 0 |
| eb6385244cd4c3d559ac65437292572ae69e5afb313662e32b6d3c7e5be0b609 | StormAttack service-DLL hijacker | MALICIOUS | 3 / 0 |
| 59e4d5d3290f082329076041e4bc34ead3636ab43eba31ba4700f89247dcd806 | Eupdate Helper 4.0.1 update mirror | BENIGN | 0 / 1 |

Counts include embedded/unpacked descendants, deduplicated by trait ID.
They describe YAML findings, not a change to the independent ML models.

## NtHook / safemon

Carved PE headers occur at 0xdc50 (NtHook driver), 0x153d8 (StartDriver),
0x169d8 (safemon DLL), and 0x57b18 (logon launcher). The driver contains
additional images in its data section; their APIs must not be attributed to
the driver's own executable code.

Rizin confirms:

- The installer registers a kernel-driver service at VA 0x00ff1770 and
  launches `rundll32.exe safemon.dll hook2` at 0x00ff2b0e.
- The driver intercepts syscall results. At 0x00013446 onward it traverses
  linked directory records, compares their names, then truncates links or
  copies following records over matches at 0x000134b8..0x000134d0. This is
  concrete directory hiding, rather than directory-enumeration imports.
- The DLL polls virtual keys at 0x1000e366, tracks modifier/key states,
  assembles text, handles backspace, and appends `<Enter>\r\n` for key 13
  at 0x1000e468. It also collects clipboard contents through dynamically
  resolved GetClipboardData (0x10010a30), uses GDI bitmap transfer
  (0x10011150), and injects a DLL with a remote LoadLibrary thread
  (0x10005eb0). Its Microsoft version identity is unsigned.
- The installer's two TerminateProcess calls, at 0x00ff3347 and 0x00ff596f,
  both consume GetCurrentProcess. They belong to runtime failure handling,
  not a demonstrated antivirus-killing loop.

Retain directory-hiding and injected-surveillance hostile findings. Retire
`unsigned-embedded-driver-installer-security-process-killer`: a security
process-name survey plus CRT self-termination cannot prove killing defenders.
Retire `unsigned-embedded-pe-driver-service-privileged-loader`: unsigned
embedded drivers, debug privilege and service metadata establish no unwanted
persistence by themselves. Retire `unsigned-wininet-dynamic-remote-thread-stager`
and `multi-pe-urlmon-download-carrier`: their unlinked API references do not
establish a downloaded buffer/path reaching execution, and can come from
nested images. Their constituent capability and format traits remain.

## StormAttack

Rizin confirms that the outer program constructs a System32 DLL path, writes
LanmanServer's ServiceDLL registry value at 0x0040133e, and allocates/writes
remote process memory before starting LoadLibraryA with CreateRemoteThread
at 0x0040123d. It also installs an Active Setup stub path at 0x00401a4b and
has self-delete cleanup. These are concrete hijacking/injection behaviors.

The embedded PE at 0x5060 carries the Storm DDoS DNS banner, welcome banner,
and STORM command-format constellation. Much of its code and resource data
is zero-filled: the identity finding is not evidence that a DNS flood actually
executed. Retain the three existing findings: LanmanServer hijack, StormAttack
injector identity, and StormAttack module identity. No YAML change is needed
for this specimen; do not infer Remcos, WannaCry, or Elex from its filename.

## Eupdate Helper

UPX 5.2.1 expands the 61,133-byte file to a 138,445-byte PE. Version resources
name Eupdate Helper 4.0.1.0, yztcsn / bbs.vc52.cn. Rizin confirms a fixed-ESET-
upstream update mirror, account-list acquisition, HKLM Run registration,
port-conflict termination, and executable padding/relaunch.

The code rejects `.signed` request paths with HTTP 404 at 0x004146c7 onward
and filters [SERVERS], [LINKS] and [HOSTS] sections at 0x00417c40. This changes
mirror routing/content; it does not patch ESET verification code or establish
acceptance of attacker-modified detection modules. No malicious replacement,
local credential theft, surveillance, remote-command dispatcher, or destructive
purpose was established. Its self-update dialog at 0x00412c6e requires IDYES
(6) before replacement. A future downloaded replacement is not present here.

The string decoder at 0x00416bb0 uses
`output[i] = input[i] XOR key XOR ((31*i+7) & 255)` for remote account-service
configuration. This is configuration decoding, not a hidden executable stage.
The account service supplies credentials; the sample does not harvest local
credential stores. Update endpoints are not treated as C2 solely by name.

The file genuinely relaxes certificate verification at 0x00413784 using
WinHttpSetOption(31, 0x3300). The separate call at 0x00414b43 configures option
84 with 0xa80 (TLS protocol selection). Preserve the precise certificate
capability at notable, consistent with other TLS-configuration traits.
Port-owner termination is likewise notable maintenance behavior; its matcher
contains no unauthorized/security-product target. Preserve suspicious
self-image hash rotation as the one unusual behavior requiring investigation.

Replace the signature-suppression objective with a neutral ESET manifest-filtering
relay profile under communications/proxy/relay. Remove its derived hostile
hash-rotation, port-kill, and Run-key composites: their shared hostile admission
was unsupported. Existing neutral rotation, termination and autorun traits
already describe these behaviors. No product-name exception is added.
Also remove the two endpoint-fetch composites: URL/client co-occurrence proves
neither a download nor suspicious purpose; their Eupdate product-name veto
made a harmless rename produce two extra suspicious findings. The underlying
IP, custom-port, URL and HTTP-client observations remain notable.

An external Dr.Web entry describes matching Eupdate behavior as a downloader:
https://vms.drweb.co.jp/virus/?i=34875111 . This is corroboration of behavior,
not proof of a hostile payload. The supplied tria.ge pages were inaccessible
to the web reader. Existing repository notes on other Eupdate hashes treated
mirror filtering as inherently hostile; this review requires evidence of
malicious substitution or a client verification bypass before that conviction.
BENIGN here includes non-malicious licensing/riskware functionality and does
not assert vendor authorization or that future updates are trustworthy.

## Checks

Run `atomscan --no-update --mode slow --follow=none -f json <sample>` and
`cleave facts <sample>` for each original path. Inspect carved images with
`cleave facts` and Rizin `aaa`, imports, strings, cross-references and function
disassembly. Use `upx -d` solely for offline unpacking.

Seven focused controls were generated in session scratch storage and analyzed
with `cleave --traits-dir . --format json`:

1. Unpacked mirror: relay profile and exact certificate-options trait present.
2. Product/IP renamed mirror: same behavioral findings; zero hostile and one
   suspicious trait, independent of vendor metadata and endpoint address.
3. Replace `.signed` with `.unused`: relay profile absent; TLS trait retained.
4. Change the option-31 immediate to 84: certificate-disable trait absent;
   relay profile retained.
5. Replace `<Enter>\r\n` with `<Space>\r\n`: the surveillance composite is absent.
6. Unmodified safemon DLL: the surveillance composite remains present.
7. Rename the packed mirror's product resource: zero hostile and one suspicious
   trait, with the relay and TLS capability retained in the unpacked child.

The valid-external-IP rename control initially activated three additional
hostile findings hidden by an Eupdate identity veto. Retire the raw-IP runtime
WinHTTP autostart and execution composites and the direct-IP hash-rotating
updater composite: none binds the downloaded bytes to execution or establishes
an unwanted result. Also retire the UPX/unsigned WinHTTP runtime-downloader
and shell-dropper composites; compression plus an HTTP client and launcher
is ordinary updater behavior. This removes the root causes rather than adding
another vendor exception. Concrete capability traits remain available.

No binary fixtures or sample judgment markers are stored in this repository.
