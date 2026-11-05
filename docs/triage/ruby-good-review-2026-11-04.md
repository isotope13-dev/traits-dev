# Ruby endpoint review — 2026-11-04

Review in progress. Initial slow scans of 24 standalone files have no severe
traits, but several require further work before any classification is recorded.

- `1a3bb85802e3` is an implemented Metasploit local privilege escalation module:
  it uploads an exploit and generated payload and runs the exploit to execute
  the payload. The separately referenced Python exploit is not embedded in this
  source. The module itself is dedicated attack tooling; two hostile traits detect
  staging and invocation, validation passed, and it was moved to bad.
- `4c9be1634f2d` builds a Meterpreter reflective DLL stage, configuration,
  and x86 execution stub. It is dedicated post-exploitation tooling; two hostile traits detect
  reflective staging and random-prefix obfuscation, validation passed, and it
  was moved to bad.
- `00df3520ce77` orchestrates credential/browser harvesting, encoded data
  exfiltration and execution of fetched commands using separately imported
  helpers. Its own calls establish dedicated post-exploitation orchestration;
  do not claim the absent helpers' internal implementations were examined.
  Two hostile traits detect harvesting/exfiltration and remote-command
  execution, validation passed, and it was moved to bad.
- `ff7bd4f4e9c3` is an inert Metasploit class skeleton whose exploit method
  only prints a status line; its name and superclass alone are not proof of an
  implemented attack.
- `d143956e5014` is a NETCONF device information and configuration collection
  script with hard-coded benchmark target and credentials; its named command
  routines issue fixed operational queries and a snapshot request, while its
  configuration edit is empty. Its endpoint ruling needs a complete review of
  whether its actual behavior is ordinary administration or reconnaissance.

The three new detections were tested against controls with their key attack
actions removed; none matched. Local snapshots were hash-verified on moving.

`9700d48953b1` is a JSP backdoor WAR builder: it reads a separate payload,
substitutes host and port, writes the configured JSP and web descriptor, and
packages the archive. The payload template is not embedded; the builder is
itself dedicated backdoor creation tooling. Two hostile detections identify
configuration and packaging, and a control without packaging does not match.
Validation passed, Hopper recorded bad, and the snapshot was hash-verified.

Seventeen standalone files were reviewed and confirmed good: a print-only
exploit skeleton, tests, gem specifications, Ruby configuration, a generic
shell executor, BetterCap target and autoload helpers, and notification-review
helpers. Their own implementations contain no executable exploit or dedicated
attack payload. The fresh slow scans have no severe findings; validation
passed and Hopper confirmed the labels. The BetterCap launcher, packet-cookie
parser, and NETCONF script remain under review, as do all package archives.

`9fd8bedc0a4d` is the NetBSD rex-powershell package (XZ despite its `.tgz`
name). It generates PowerShell AMSI and script-logging bypasses and includes
shellcode-loading templates that decode, change memory protections, and create
threads. The fresh scan identifies these behaviors with hostile traits in
multiple directories; validation passed and it was moved to bad.

Three network-related files were recorded dual-use: `74ddb9d60fe2` starts the
BetterCap network interception framework supplied separately;
`aafc61ae8017` extracts HTTP Cookie headers from packets and logs them; and
`d143956e5014` connects to a hard-coded NETCONF endpoint, gathers device and
security configuration and runs fixed administrative requests. The latter's
actual commands are fixed operational queries and snapshot requests, not the
arbitrary WMI execution suggested by its filename. The cookie parser now has a
suspicious trait describing packet-cookie logging, with a negative control
without logging. Validation passed and all three snapshots were hash-verified.

Six gems were confirmed good: Vagrant `66c6955cf15f`, Kitchen Dokken
`7548c1f34315`, Kitchen EC2 `8bbb7dade2c8`, ClickHouse client
`e30009d2e3b2`, Inline Forms Installer `ea0681d1c8ba`, and development tools
`f4573c2ec4be`. Their contents and executable indicators were reviewed; fresh
scans report no severe findings. Validation passed and Hopper confirmed each
label; the unknown snapshots were hash-verified and moved to the good pool.

`13ac0ce8ee71` is Puppet source containing an executable access-control
regression test that sends a fabricated report for a different node using the
server's certificate. Although the test expects the server to reject it, the
request implements the bypass attempt and is attack code under this review
policy. Two hostile traits describe the forged request and attempted identity
bypass, and removing the HTTP request from a control eliminates both. A fresh
archive scan and validation passed; Hopper recorded bad and the snapshot was
hash-verified on relocation.

The remaining good archives are UNetbootin `ddeaf68583bf` (one warning for
its packed UPX executable), Homebrew formulae `8f601b97cb66`, Ruby 3.3.8
`e2e1233ad275`, Ruby 4.0.3 `67035481fbd1`, Relay `b84313a4d4a5`, Woods
`f67551cc8a3b`, and Azure IoT Toolkit `64e8b38f6061`. The Ruby releases'
security specs exercise library input validation; their inputs are not remote
exploit implementations. Woods has an opt-in console evaluator guarded by a
confirmation callback; one new suspicious trait records this capability, and
removing the evaluation call from a control prevents the match. Its credential
scanner redacts secrets from responses. Fresh scans and validation passed;
Hopper confirmed the labels and unknown snapshots were hash-verified.

Two misleading suspicious primitives had labeled a routine `File.binwrite`
and a long RubyGems-prefixed identifier as exfiltration or a credential. They
were relocated to neutral micro-behavior traits and existing combinations were
updated to refer to them. The Ruby releases and Homebrew archive scan clean.

`f1a84257a94e` is a Metasploit framework Debian package. Its 35,841 scanned
components include exploitation modules, reverse and bind shells, web shells,
and security-control bypass code. The archive-level scan reports 59 hostile
traits across multiple directories. Validation passed and the package was
moved to bad with a hash-verified snapshot.

Ruby total: 30 good, 7 bad, 3 dual-use.
