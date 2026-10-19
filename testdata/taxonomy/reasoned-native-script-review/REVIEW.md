Reasoned review of three samples

All verdicts below come from static execution-path analysis. No specimen was
executed and no live payload endpoint was fetched. The supplied reputation
labels were leads; the referenced reputation pages were unavailable during
this review.

`5f4838a39b064a0165cc673526d2d7a0be456d259b1f392964ed4dd2084a194d`
— MALICIOUS, batch/PowerShell registry-cached script loader. Remcos attribution
is not established by the available stage.

The batch stores PowerShell in an environment variable and pipes it to a hidden
32-bit PowerShell, falling back to System32. Removing constant-expression noise
reveals two decoders. Numeric arrays subtract the repeating ASCII key
`Sympodium` and convert the results to characters. This recovers `iex`, the
Base64 conversion expression, the per-byte XOR expression, and the character
join. Base64 literals then XOR with that same repeating key. Dynamic calls
invoke the recovered expressions; this is executable reconstruction rather than
an incidental Base64 string.

The recovered program creates `Msxml2.ServerXMLHTTP.6.0`, issues a synchronous
GET to `hxxp://thetamarindleafresidency[.]com/brikvvedes.ocx`, and on HTTP 200
caches responseText in HKCU `Nederdels\Filmsprog`, value `Lokalplanstridiges`.
It retries until the registry key exists. It reads the cached value, Base64
decodes it, converts bytes to ASCII, extracts 33,859 characters starting at
163,802, and passes that script to the recovered `iex`. Registry caching is
not an autostart mechanism. The concealed external script acquisition and
execution establish a malicious stager; the unavailable final stage limits
family attribution. The YAML correctly expresses two suspicious concealment
patterns rather than inferring a hostile family from padding or hidden piping.

`bf7562c880967fc2afca8669b0ef1cdfa8c273d5338300c455418c0c234d23a4`
— MALICIOUS, unstripped ARM Mirai-derived multi-vector flood bot with NeTiS
and LZRD branding.

Rizin disassembly traces `main` at 0xf81c through table initialization,
`attack_init` (0x8620), `killer_init`, watchdog startup (0xf5dc), and daemonizing
forks. `resolve_cnc_addr` at 0xf594 sets an external controller address,
176.65.139[.]143. The receive loop reads a two-byte network-order frame length
and passes received bytes to `attack_parse` at 0x8328 (call at 0xff4c). The parser
decodes duration, vector, targets, and options, and calls `attack_start` at
0x822c. That routine forks a timed worker, dispatches the selected function
pointer, and starts a timer child which kills the worker with SIGKILL. Registered
handlers include UDP plain at 0x9340 and TCP SYN at 0xbf74, among numerous
protocol-specific implementations. The UDP worker connects target sockets and
repeatedly sends payloads; TCP workers construct packet headers and checksums
and send in loops. This is controller-directed resource abuse, not a networking
library's vocabulary.

`table_unlock_val` at 0x10240 applies the four bytes of `table_key` by XOR; the
net transform is XOR 0x22. Decoding confirms watchdog paths, the Source Engine
query payload, and LZRD strings. The watchdog child opens devices and repeatedly
issues WDIOC_SETOPTIONS with disable-card value 1 and WDIOC_KEEPALIVE. The
process killer reaches `kill` at 0xf56c after its process-selection logic.
GPON evidence consists of retained source/PID names, with no GPON scanner init
path. SSDP, browser headers, and Source Engine query text are retained table
content; no corresponding SSDP/HTTP/Source-query attack handler was established.
Those references must not become active scanning, spoofing, or specific flood
claims. The Source-query hostile rule now requires its actual handler-name
leg, and the redundant ARM/HTTP classification was removed.

`57a418763e3290646433897b4bb1c5d564c5c80b8b72899636e4336af422f239`
— MALICIOUS, NanoCoreFinal-branded managed RAT impersonating Windows Update.
The namespace is not proof of canonical NanoCore provenance.

Parsed CLR method bodies identify entry token 0x06000033 (`Program.Main`, RVA
0x2910). Main installs copied executable paths through HKCU Run values and a
logon scheduled task, launches account-create/admin-group-add commands, writes
the ms-settings shell association and empty DelegateExecute value before
launching fodhelper, and attempts to disable Defender protection with hidden
PowerShell. It calls NtSetInformationProcess with class 29 and an enabled
boolean. Success depends on privileges and Windows controls; attempts and
references are distinguished from successful effects.

Keylogger Start (0x20cc) installs WH_KEYBOARD_LL with HookCallback (0x21dc).
The callback reads the key code, adds timestamp and foreground-window title,
and appends to a StringBuilder. SendLoop (0x22e8) flushes that buffer to a local
keylog and a Base64 KEYLOG record. Other started workers read clipboard memory,
capture the primary screen, copy Chrome/Edge Login Data/Cookies/History stores,
and enumerate document/key/wallet extensions in user folders. SendFile
(0x37f0) reads file bytes and constructs a Base64 FILE record. Browser store
copying is established; password decryption is not. The Wi-Fi helper attempts
`wlan show profiles key=clear`; successful password recovery is not established.

The HTTP task worker at 0x3a24 reads `/cmd` responses, executes nonempty tasks
with hidden `cmd.exe /c`, captures stdout, and sends a CMD_OUT record. Its
`download` task actually sends an existing local file. The reverse-shell
worker at 0x38bc creates a TcpClient on port 5555, starts hidden cmd with
redirected input/output, and starts complementary network-to-stdin and
stdout-to-network loops (methods 70/71, RVAs 0x3844/0x3880). SendToC2 (0x3c78)
XORs UTF-8 records with a 32-byte key, Base64 encodes them, and constructs an
HTTP GET `/log?d=` request. These paths substantiate the existing surveillance,
persistence, reverse-shell and evasion findings and the new HTTP command rule.

Configuration includes `http://` in C2_DOMAIN and then prefixes it again for
HTTP and passes the scheme-bearing value to TcpClient. This can prevent intended
C2 operation. Static analysis establishes implemented attempts, not successful
network sessions. AMSI_Patch and ETW_Patch are merely reporting strings. The
ProcessHollowing message follows remote allocation/write/thread creation in
notepad, using six bytes that return 100; no image hollowing is implemented.
No new AMSI, ETW, hollowing, or microphone-capture objective was inferred.

Controls and placement

Run `python3 testdata/taxonomy/reasoned-native-script-review/check.py`, optionally
passing the managed sample path to test three missing-role mutations. All files
are scanned as data in temporary directories outside testdata, avoiding test
path exclusions. The tiny ELF fixtures contain only a return instruction and
synthetic names/templates; they are never executed. They test reference
classification and transport cardinality, not dynamic attack execution.

The controls cover ordinary hidden PowerShell with indirect calls and dummy
hex/math operations, a character codec without eval, padded indirect decoding,
URL query construction, retained GPON/SSDP/watchdog references, one flood
transport versus two, and removal of the RAT executor, response-reader, or output
record role. Positive and negative role tests accompany the real samples.

Relocations retain effective scope except where corrected explicitly: GPON is
now an ELF string-table property, watchdog configuration no longer admits an
executable path as configuration, and protocol-method names no longer claim
multiple methods from one match. All exact YAML consumers were updated. The
User-Agent query assembly trait moved to URL/query during the destination budget
audit; its two exact consumers were updated and a source control verifies the
same observation. No directory budgets were raised and no new taxonomy leaf was
created. Final verification uses atomscan for each original path and make
validate after judgement markers are written.
