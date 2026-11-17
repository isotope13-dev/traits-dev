# PyPI dataset triage notes

These notes describe the collected archives, not every published version of a
package. Scans use `atomscan --no-update --follow=none --format=json-full
--zip-password infected`. The scan class is separate from the criticality of
individual trait findings.

## E batch

The ten `example-package-sthnck` archives without hostile findings contain
sample-project sources, warning-free trivial package code, and packaging
metadata. Their `pwned` files are empty or only call `print()`. Their Git packs
have three different binary encodings but the same 593 object IDs, and every
archive points to the same main-branch commit. All 198 blobs are reachable from
that commit. A marker search over those blobs found only ordinary release
workflow uses of a PyPI secret; an AST survey of 88 historical Python blobs
found no dynamic execution or network calls, with one syntax-invalid setup
revision. This is a targeted history check rather than proof that every
historical file is benign.

## F batch, partial

* `ffmpge`: package metadata and an inert setup file; no package code present.
* `figlets` versions 1, 3, and 4: archives contain no files.
* `flaask` versions 0.0.1 and 0.0.2: warning modules and metadata; no
  exfiltration or loader observed in the collected code.

All 61 F archives were scanned. The list above covers the six that lacked a
hostile trait in that scan; review of the other findings remains open.

## G batch, partial

All 45 G archives were scanned. `genz-translator` 9000.0.1 executes an inline
socket reverse shell during installation; a trait now identifies that call.
The `gnosis-py` and `gradio-videotimeline` 0.0.0 archives contain dummy modules.
`grandslam` prompts for Apple credentials, derives an SRP password value and
uses Apple's authentication endpoints. It fetches anisette data from a separate
server; the reviewed code does not send the password to that server. Its
authentication behavior is sensitive, but that observation alone does not prove
credential exfiltration.

The 21 `genz-translator` versions were rescanned after correcting the custom
index and shell-code rule: it no longer treats commented-out commands as live.
Version 9002.0.1 attempts to write shell code through a file opened with the
default read-only mode. Version 9030.0.1 has that shell write commented out,
but invokes pip against a custom index with an inflated version; 9016.0.1
invokes pip uninstall from its initializer. Separate traits now cover those
observed behaviors. All 21 versions retain at least one hostile trait. Their
archive verdicts were already hostile before the new traits.

## H batch, partial

All 61 H archives were scanned. `hellotesthim` 0.1.1 contains a layered
Windows browser credential collector; `hmac2` 0.0.2 and 0.0.2rc0 contain an
encoded HTTP command agent. Both now have hostile findings. `httpxontop` 1.0
contains a temporary remote-code loader, and `http3-client` 1.0.17 defines a
remote-code loader whose thread is constructed but not started; both now have
hostile findings. `huluquests` 0.0.3 contains an encoded marshal executable
loader and now has a hostile finding.

`herewalletbot` 0.1.0, 0.2.0, and 1.0 contain the same wallet automation
source. It prompts for a seed phrase and supplies it to a Telegram wallet UI;
no separate exfiltration endpoint was observed in that source. The two
`hackerone-app-sdk` versions 0.17.0 and 0.18.0 contain empty package modules.
`httprequesting` 1.1.1 contains an initializer and script that run a local
`my_script.py` only when invoked as the main program; that file is absent.
`hugginglega` 1.0 imports `transformers` and runs `id` if the import succeeds;
the collected module contains no further payload. The remaining collected
`http3-client` versions have trivial setup or print-only code, except 1.0.18,
whose initializer imports a missing `main` module. Version 1.0.7 advertises
an entry point whose module is absent.
Review of other H findings remains open.

## I batch, partial

All 36 I archives were scanned. `importlib-metadate` 99.99 calls a setup
function that posts host details, directory listings, `/etc/passwd`, and shell
history; it now has a hostile finding. `imap-utisl` contains package metadata
and setup code but no package payload. The `imad213` scripts prompt for a
username and password and submit them to multiple third-party follower-service
sites. Version 2.0.4 stores the supplied credentials locally and wraps its
source in Base64. Its decoded source fetches a status value and can launch
screen-clearing or browser-opening commands. The Base64 download-and-launch
trait no longer combines unrelated evidence across archive members or matches
that code. It still detects the encoded downloader in `invokehttp` 2.5.5 and
has direct-call and non-launch controls. Its aliased-call coverage is limited
to the alias observed in that sample; other aliases need data-flow-aware
coverage. A rescan of all 86 archives that historically matched that rule
found at least one hostile trait in each. The `xinference` 2.6.1 report warned
that its uploaded member list was limited to 256 of 295 entries; this rescan
does not establish a complete review of that archive. Review of other I
findings remains open.

## J batch, partial

All 26 J archives were scanned. The eight `just4testlm` archives without a
hostile trait (0.2.0 through 0.6.0, 0.8.0, 0.9.1, and 0.9.3) contain a
hello-world module and packaging metadata. Other versions have different
contents; their findings require separate review.

## K batch, partial

All 35 K archives were scanned. `kube-health-tools` 1.0.10 and 1.0.11
launch a temporary downloaded binary with piped configuration on import;
both now have a hostile finding. Versions 1.0.8 and 1.0.9 provide the same
download, launch, and cleanup behavior through `main`; 1.0.8 requires an
environment-provided configuration. Both now have hostile findings.
`kersa` 0.1 reconstructs and runs a mining
installer during setup and now has a hostile finding. `krbutils` 1.0.0
writes user and host information under `M:\\flag` during installation; the
archive does not establish whether the drive is mapped or remote, and its
deployment context needs further review.

## L batch, partial

All 181 L archives were scanned. `larpexodus` 0.1 downloads and starts an executable
through PowerShell in an install hook; it now has a hostile finding. The
`lala6992` versions reviewed so far create local host/user marker files or
contain simple package code; 1.2.0 targets `M:\flag`, whose mapping is not
established by the archive. `lanchain-openai` 0.0.0 contains a dummy module.
Several `libgui`-family packages contain encoded PowerShell downloaders and
already have hostile findings; this observation is based on sampled members,
not a complete review of the family.

`license-utils-kit` 0.1a0, 0.1a1, and 0.1b1 and `logutilkit` 1.0.1 download
an archive, select an executable with a platform-specific system service name,
and launch it from their update helper. They now have hostile findings.

Among the first 61 L archives with an encoded PowerShell command in setup,
decoding the command bytes produced four distinct scripts. Each downloads an
executable and invokes the downloaded path; all 61 scan results contain at
least one hostile trait. This grouping covers only the setup command, not all
members or other characteristics of those archives.

Five sampled `libid`-family setup payloads (`libida`, `libide`, `libidee`,
`libideee`, and `libidi`) decode to Python that writes and starts an embedded
Windows PE. The outer scans flag the loaders. A separate scan of the five PE
files produced a hostile WhiteSnake signature for `libideee`; the other four
were classified benign. Those four contain managed command-processing symbols,
with webcam and spreading-related names in some, and need further reverse
engineering before drawing a verdict about the embedded programs.

## M batch, partial

All 129 M archives were scanned. `manda-tu-cv-a-secureit` sends a network
interface profile over a socket in its install hook. `mumuzi1` 1.5 and
`mumuziyyds` 1.0, 1.1, and 1.5 send an encoded host profile in an HTTP query;
versions 1.2 and 1.3 use loopback addresses. `muxf` 0.0.1 posts the hostname
to a hard-coded WeChat webhook during installation. These externally directed
behaviors now have hostile traits. The decoded `msfpath` payload contains a TCP
remote shell and file-transfer commands, but its archive still needs better
detection of the layered encoding. The package's documented import of `check`
executes a Base64 and character-substitution wrapper, followed by hex and
repeating-key XOR layers; the outer file currently has suspicious execution
findings, including a new inverse-table/Base64 execution finding, but no
hostile trait identifying the decoded shell.

`marshmellow` 1.0.0 and 1.1.0 and `marshmellows` 1.0.0 silently collect
user and host details during installation and write them under `M:\\flag`.
The archives do not establish whether that drive is remote. Their archive
model verdicts were already hostile; they have no hostile trait in the current
scan. `musl-dev` 0.0.0 and `my-package-jiecub3` 1.0.0 through 1.2.0 contain
dummy or example code. `moneyprinter-api` 0.1.0 runs `./script.sh` from the
working directory during setup, but the collected archive does not include
that script. `mlc-llm-nightly` 99.99.99, 99.99.100 and 99.99.102 contain only
packaging and collector metadata. `mlc-ai-nightly` 0.0.1 contains sample setup and test code without an
active install hook. `mastowrapper` describes a Mastodon wrapper but contains
a differently branded client; its explicit `connect` method sends user, host,
public IP and supplied credentials to the client's backend. Its purpose and
the discrepancy warrant further review.

`modernreqs` 2.3.5 executes Base64-encoded source that gathers Telegram Desktop
session files, archives them and uploads the archive through a bot. The archive
already had hostile upload findings; a new trait highlights the encoded
Telegram Desktop and `tdata` references alongside the upload code. The trait
reports co-occurring evidence rather than proving data flow.

## N batch, partial

All 33 N archives were scanned. `networkx-match` 0.1.0 and 0.1.1 send a
literal TCP greeting to a public address in an install hook; both now have a
hostile trait. The socket code in `networkx-match-algr` and
`networkx-match-ssss` is commented out. `neverinstallme` 0.1.6 reads
`/etc/passwd` and writes it to a hidden configuration file if the file is
absent; 0.1.7 fetches a URL and writes its content under the same condition.
Both actions are invoked by build or installation hooks. No external transfer
of the password file was established, and the 0.1.7 endpoint's purpose is
not established. A new suspicious trait highlights the passwd-open and hidden
write clues in 0.1.6 without asserting a data flow from those clues alone.
Versions 0.1.0 and 0.1.1 contain hello-world code; 0.1.3 through 0.1.5
create a hidden config with a static comment. `node-hill`, `noed-hill` and
`noed` contain setup and metadata files without package code.

## O batch, partial

All 31 O archives were scanned. `otr-utils` 4.1.0 and 4.1.9 contain
packaging metadata but no Python source, unlike 4.1.1, which posts host
information to an OAST endpoint. `opentelematry-api` and `oraceldb` write
user and host marker files under `M:\\flag`; whether that drive is remotely
mapped is not established. `oxeru` 0.1.4 requests a fixed URL during its
install hook; its security proof-of-concept metadata and registered callback
now have a hostile trait. The archive was already classified hostile by the
model. The endpoint's response and purpose are not established. The related
`oxeru1` and `oxeru2` packages add a socket-connected shell; `oxeru3-test`
sends host and uptime details over a socket during installation.

## Q batch, partial

All 17 Q archives were scanned. `quasarlib` 1.0.7 and 1.0.8 include the
same XOR-encoded Windows DLL, disguised as a Python source file. Their `load`
function decodes a file, constructs an encoded `rundll32` command, invokes
its `CalculateSum` export, and removes the decoded file. No internal call to
that function was found. The decoded DLL matches an existing Lazarus
npmLoader signature. Both archives now have a hostile loader trait; copies on
elrond have verified SHA-256 hashes. `quicly` 1.0.99 and 1.1.2 through 1.1.6
share an identical decorator module. For one hex-encoded Redis key, it
substitutes an existence result and a fabricated record and suppresses writes;
a new hostile trait identifies the conditional interception. A separate
wrapper replaces hash input with random UUID bytes and delays execution when
the outermost script name has a particular prefix. These versions already had
hostile findings before the new trait.

`quicly` 1.1.16 lacks a hostile trait. Compared with 1.1.2, its setup script
removes the install hook that posts host details to a WeChat webhook, and its
decorator module removes the interception functions. Its unchanged Redis and
hash modules still reference removed decorator names, which can cause imports
of those modules to fail. A survey of the remaining Python files found ordinary
client, server and utility functionality; complete behavioral review remains
open.

## P batch, partial

The first 60 of 381 P archives were scanned, and review remains incomplete.
`pandasprox` 1.0.1 posts shell-derived process and network inventory to a
webhook in setup. `pepequests` 0.0.1 and 0.0.2 contain a base64-encoded
marshal loader that fetches and runs a Windows executable. `ploghandle`
uploads an encoded host and interface profile when setup evaluates its version.
All four now have hostile traits and verified copies on elrond. `pandaai`
writes a host/user marker to `M:\\flag`; the drive mapping is unknown.
`peptest` 1.0.0 and 1.2.0 post an installation notification and Python
version to a webhook; both now have hostile install-callback findings and
verified copies on elrond. Other P misses still need individual review.

The next 60 P archives were scanned. The two
`pplgdfhuighsdfyisfdty2` and `pplgdfhuighsdfyisfgfd` archives post the
Google Cloud service-account listing to a webhook; both now have hostile
findings and verified copies. The related `pplgdfhuighsdfyisfdty` archive
requests a service-account token and already had a hostile finding.

`pxz` 1.1.2 through 1.1.13 contain an empty package initializer and wheel
metadata in the archived contents; version 1.1.14 instead contains an
import-time host-profile upload and was already detected. The `pip-doom`
versions 0.1.0 through 0.1.10 invoke a bundled terminal Doom program during
installation or build. The four bundled executable hashes are identical
across the versions, and Atomscan classifies those four binaries benign;
this is not a complete reverse engineering of their native code. `ptmpl`
0.2.12 has a commented-out encrypted remote-code loader; its active install
hook prints data from an IP-information service. Its separately invoked
command downloads and runs remote scripts, so the context and script contents
need further review. Decryption of the commented ciphertext was performed
without executing it.

The third group of 60 P archives was also scanned. Each has at least one
critical trait; their full behavior and coverage have not yet been reviewed.

The fourth group of 60 P archives was scanned. `pyadd` 0.1.3 attempts to
fetch an executable from a Discord CDN URL with PowerShell and execute the
downloaded path during import; it now has a hostile finding and a verified
copy on elrond. Its 0.1.0–0.1.2 siblings already had hostile findings.
`pycord-self` 1.0 and 2.0 send the Discord login token in a disguised HTTP
header to a third-party address and start a socket-connected shell. Both now
have separate hostile findings for these behaviors and verified copies on
elrond. `pycolorz` 0.0.1 contains setup and metadata but no package module.

The fifth and sixth groups of 60 P archives were scanned. `pycryptoconf`
1.0.3 and 1.0.4 contain the same XOR-encoded DLL, which matches JPCERT's
npmLoader signature after decoding. Both now have a hostile embedded-payload
finding and verified copies on elrond. The 1.0.3 Python loader has an
indentation error; the 1.0.4 loader uses the same key for a DLL and command
that require different keys. Neither defect changes the embedded DLL bytes.
`pylibscate` 1.1.0 unwraps to a W4SP credential stealer; the packed carrier
now has a hostile finding and a verified copy. `pydefender` 1.0.0 and 1.0.3
contain a packed Windows startup downloader and now have hostile payload
findings and verified copies. The 1.0.3 entry module first imports a missing
`main` symbol, so its loader may stop before reaching the payload.

`pyprotector` 1.0.3 downloads a Python script, creates a Windows Run entry
for the downloaded path, and launches that path; it now has a hostile finding
and a verified copy. `pyqubee` 12.1.1 posts its host profile to an OAST
endpoint during installation. `pytabtrust` 9999999.1.1 sends an encoded
login name and working directory to an external endpoint during installation.
`pyrologin` 2.6 downloads and extracts an archive, then starts a hidden
Python process through WScript from setup. All three now have hostile findings
and verified copies on elrond.

`python-ledgercommon` 1.56.3 through 1.56.8 contain only wheel metadata in
the archived contents; other versions contain host-reporting code and must be
judged individually. `pyprettifier` 0.1.0 contains an emoji lookup utility.
`pynalc` and `pythno` contain setup and metadata but no package module.
`pycolorz` 0.0.1 is similarly missing its package module. `pycrypterexe`
1.0.9, 1.1.0, and 1.1.1 contain an empty encryption function or hello-world
code; some imports refer to missing modules. `pycryptexe` 1.1.3
and 1.1.4 contain an encoded install command that fetches a script from
localhost and pipes it to Bash. Both now have hostile execution-PoC findings
and verified copies on elrond; the local server contents are unknown.

`pycrypterexe` 1.0.5 attempts an install-time POST to a literal
`your_webhook_url_here` placeholder, with no other Python payload in the
collected archive. Its broad webhook hostile trait was removed, although its
model verdict remains hostile. Versions 1.0.4, 1.0.6 and 1.0.7 have
webhook-shaped addresses and retain their registered install-hook finding.
`pyprettifier` 0.1.4 and 0.1.5 include a decorator that posts the user's home
path to an embedded webhook when the decorated function runs; they now have a
specific finding. Version 0.1.4's decorated module has a syntax error, which
prevents its ordinary import path from reaching the helper.

`pingdomv3` 1.0.0 has a Pingdom API client and an inert logger; 1.1.0
replaces the logger with Base64 source that fetches and executes remote Python
when `JENKINS_URL` is present. Version 1.1.0 already had hostile findings and
now also identifies the Jenkins-gated loader. A broad Base64/HTTP rule was
restricted after it flagged a fetch-and-print control: the three historical
samples matched by that rule retain hostile findings. Related generic rules
still flag loopback and placeholder remote-execution controls; those need
separate review. `pydantics` 1.0.0 writes user and host details to `M:\\flag`
during installation; the archive does not establish the drive's mapping.

All 381 P archives have now been scanned. The last 21 each had a critical
trait at scan time; a critical finding alone does not complete their review.

## R batch, partial

All 118 R archives were scanned; behavioral review remains incomplete. Ten
`reques*`/`requzsts` packages execute different Fernet-encrypted payloads in
registered install hooks. Authenticating and decrypting each without executing
it showed a fetch-and-exec from the same external service. They now have a
hostile install-loader finding and verified copies on elrond.

`requests-darwin-lite` 2.27.1 and 2.27.2 extract and execute an appended Mach-O
only for a particular macOS hardware UUID. Version 2.28.0 omits the loader but
retains the identical Mach-O in the PNG. The extracted Mach-O separately
matches obfuscated beacon and tasking traits. All three now have a hostile
PNG-carrier finding and verified copies. `randrange` posts the process
environment, encoded by a helper in a second file, to an assembled OAST domain
from its install class. `randomized` contains a multiply encoded Linux script
downloader, and `relefpots` executes a downloaded HTTP response at import.
These three now have hostile findings and verified copies.

`reverseshell` 0.0.2 through 0.0.5 and 0.1.0 implement a TCP command and
output loop; 0.0.5 and 0.1.0 send output through a chunking helper. They now
have hostile findings and verified copies. `rippling-cli` 1.0.1 and `rtpoc1`
0.2 make import-time OAST requests, the latter in a thread; both now have
hostile findings and verified copies. `robloxapiaccess` 0.0.1 contains code
that targets Roblox cookies and Chromium credentials for a Discord webhook;
its webhook value is blank. It now has a hostile finding and verified copy.

The separate `reverse-shell` project has materially different releases.
Version 0.1 calls a localhost command shell when its `reverse_shell` module
is imported. Version 0.5 contains an installation-notification webhook
function, but its collected setup does not call it and the initializer calls
it only under a main guard. The generic hostile webhook trait now requires a
registered install hook and no longer fires on that archive. Version 0.9 calls
a host-IP notification from setup's main
guard. Version 1.0's setup has an indentation error, and its package modules
import a symbol from a partially initialized copy of their own module before
the clone-and-run code. Version 1.1's setup can clone a repository and run a
Python file; an existing hostile trait now covers this form without requiring
a pip-install command. Version 1.3 also performs that sequence. Both already
had hostile archive verdicts. Version 1.5 installs GitPython at setup module
scope and calls its clone-and-run helper under the main guard.

`reuquests` 2.28.2 adds an import-time function to a Requests initializer. It
attempts to collect an SSH private key, known hosts, shell history and regular
files in the current directory, suppresses stdout and stderr, compresses the
collected data and sends a urllib request. It can return early for a marker
file or fail before sending if a required operation raises. The earlier archive
verdict was benign; the new collection, suppression and request findings
produce a hostile archive verdict. The sample was copied to elrond and its
SHA-256 verified.

The examined `raydium`, `raydium-sdk`, `requestsx`, `r4quests`, `req7ests`,
and `req8ests` archives contain only directory entries. The two Roblox-named
archives examined contain packaging metadata and dependency declarations but
no package module. `ripe-atlas-dyndns` prints a greeting; its OAST code is
commented out. `ritch` writes a host/user marker under `M:\\flag`, whose
mapping is unknown. `rlask` 3.1.3 and `rsquests` 2.34.2 lack the `.pth`
loader found in their next versions; the compared Python files are otherwise
identical. These observations do not establish that the entire letter is
fully reviewed.

## S batch, partial

The first 60 S archives were scanned. `sagetestfour`, `sagetestthree`, and
both `sagetesttwo` archives clone a repository beneath the Windows Startup
folder and move a Python file into Startup during installation. All four now
have hostile findings and verified copies on elrond. `security-util` 0.0.1
through 0.0.3 send a Base64 host, user, and working-directory profile in a
hand-built HTTP request over TLS during installation; all three now have
hostile findings and verified copies. `salamus8` makes an install-time request
as part of its stated typosquat installation-count probe and now has a hostile
PoC finding and verified copy. The examined `salamus` through `salamus7`
variants print or write local text files; their descriptions do not establish
network activity. `selenim` contains packaging metadata but no package module.

The next 60 S archives were scanned and each had at least one critical trait
at scan time. Their setup scripts contain encoded PowerShell commands that
decode to four variants; all download an executable and invoke the downloaded
path. This grouping covers those commands, not every archive member.

The third group of 60 S archives was scanned. `set-utils` 1.1.0 replaces Web3
account constructors and includes a function that encrypts an account's
private key into transaction data, signs the transaction with that account,
and submits it. It now has a hostile finding and a verified copy on elrond.
`setdotwork` 0.7 and `setnetwork` 0.3 contain only directory entries;
`sfnt2woff-zopfli` 0.0.0 contains a dummy module. The 38 `self*` archives
in this group have five encoded PowerShell variants; each decoded command
downloads and launches an executable. That comparison covers setup commands,
not all archive members.

The fourth group of 60 S archives was scanned. `sln1550hello` 0.0.2 sends
root files matching `/f*` to a webhook from setup. `some-random-package-33`
2.3.100 reconstructs `os.system`, `wget`, and an OASTify domain from string
fragments and invokes them in package hooks. `spyme` stages files named as a
keylogger and reverse shell from a localhost service and starts the listener
on install; the downloaded payload bytes are not in the archive. These now
have hostile findings and verified copies on elrond.

`spellcheckers` 1.0.0, 1.1.0, 1.1.1, and 1.2.0 contain an import-invoked
loader that Base64-decodes and executes a local index file, but the targeted
index file is absent from those archives. They now have loader findings and
verified copies; the missing file would cause an error before decoding. Later
versions include an encoded index whose decoded content fetches and starts
remote Python, and already had hostile findings. `speech-dtw` 0.1.1 sends a
literal greeting to a private address during installation. `sol-structs`
1.0.2 and `spl-types` 1.0.4 contain identical examined Python source with
Solana data layouts and a market-data request; further review may be needed.
`siamttviews` 5.1.1 is a manually launched TikTok view-inflation tool: it takes
a video ID and repeatedly submits `play_delta=1` to the mobile stats endpoint
from worker threads. No credential theft was established. The new file-scoped
view-count composite detects this behavior; a fixture with the repeated
increment loop is hostile, while ordinary stats lookup and a single increment
remain non-hostile. The archive is now classified hostile and its verified
copy is at `elrond:/tmp/hostile/e548444c6750ea9426919552c5334b6c2eea39657f1a945d01370ac278b6a34e/2023-02-28-siamttviews-v5.1.1.zip`.

Comparing `sol-structs` 1.0.2 with 1.0.3 shows that the later version adds a
CP1026-encoded fetch-and-execute statement; `spl-types` 1.0.5 and 1.0.7 have
the same decoded stage. The 1.0.6 source has an indentation error, so its
encoded loader cannot run as that Python module. The existing finding now
describes the loader's presence without asserting successful execution.

The remaining 72 S archives were scanned. `supra-style` 0.7 downloads an
executable into Windows Startup and invokes that same path in setup; it now
has a hostile finding and a verified copy on elrond. `suyo` 1.0.0 and 1.1.1
include an explicitly invoked function that posts a fixed test message to a
webhook; the reviewed code does not establish hostile activity. `swapmempool`
1.0.8 contains a large cryptography library and an XOR-encoded Windows DLL
disguised as `utilities.py`. A defined loader decodes that file, writes it as
`config.py`, constructs an XOR-decoded `rundll32` command for its `AddNumbers`
export and removes the staged file. No internal call to that loader was found.
The DLL has packed-loader and anti-analysis findings, but its full behavior
and identity remain unconfirmed. The generalized XOR/rundll32 trait now
detects the loader; the archive was already classified hostile by the model.
`sysargvsox` 1.1.1 executes a Base64/LZMA loader on import. Static
decoding reveals routines that reset an RDP user password, report access
details, and stage a miner; the decoded module defines but does not call its
`run` function, so those routines require a later call. The loader now has a
hostile finding and a verified copy on elrond. These
are initial scan results, not a complete review of all 312 S archives.


## T batch, partial

All 197 T archives received initial scans. `thisismytest` 1.0.0
pipes Python code from a raw IP into an interpreter during setup.
`testpipxyz3` and `testpipxyz4` collect `whoami` and post the result during
installation as dependency-confusion probes. Both `testveriftest1asdlaaaa`
variants use setup hooks to post Google Cloud metadata responses to OAST; one
targets a service-account token, while the other targets the account directory.
These five now have hostile findings and verified copies on elrond.

The two `test-poc-package-for-session` samples write fixed text to a local
temporary file. `testinglmao123` prints a character, and `testerpackage123`
decodes a greeting and delay. `tosa-serialization-lib` 0.0.0 contains a dummy
module. `tlask` 3.1.3 requires further review; unlike 3.1.4, it lacks that
version's `.pth` and large JavaScript file. Initial scanning does not establish
a completed review of all archive members.


`test23414234234` 0.5 includes a nonstandard `build.pypi` containing encoded
Windows and Linux branches. The Linux branch collects Firefox login and cookie
files, screenshots and system details, then sends an archive through Telegram;
the Windows branch writes and starts an embedded executable. The archive does
not contain an ordinary `setup.py`, so normal setup invocation is not established.
It now has an encoded-indicator finding and a verified copy on elrond.

`termncolor` 3.1.0 declares and imports the unpinned `colorinal` dependency.
In the sampled `colorinal` 0.1.7, importing the package loads a bundled native
library through `ctypes` and removes its `unicode.py` source in a `finally`
block. A new archive rule flags the parent's declaration and runtime import
together. The parent's dependency is unpinned, so resolution to this sampled
version is not proven; the parent archive still receives a benign overall
verdict despite the critical chain finding. Similarly, `tryquests` imports and
depends on unpinned `stillrequestsa`; the dataset's 0.0.1 and 0.0.2 versions
contain encoded executable downloaders and already have hostile findings.
`twien` contains setup metadata and no package code in the examined archive.
`tdwtauthauthentication` 1.0.8 has a plugin-manager package but no observed
setup-time behavior; its setup imports several unused networking modules. In
1.0.9, setup adds a host profile encoded as Base64 and sends it in an HTTP GET
to a raw IP. Version 1.0.9 already scans hostile; 1.0.8 remains benign.
`test-23234231` 0.1, 0.9, and 10 contain a large setup script with a
Base64/`exec` loader and existing critical findings for Telegram stealer
behavior and document exfiltration. Versions 11 and 232 contain only empty
directory entries and remain benign.

All 109 `tp*` setup commands in T positions 61–197 decode to four PowerShell
variants; each downloads an executable and invokes its saved path. This
comparison covers setup commands only, not all members of those archives.

## U batch, partial

All 28 U archives received initial scans. `umap` 0.0.0 contains only a tiny
placeholder module; 0.1.1 contains a small Folium map helper using geographic
distance calculations and has no setup-time behavior in the examined files.
`upgini`
1.1.99, 1.1.100, and 1.1.101 send the local username in setup telemetry to the
project's service; a new suspicious finding reports the username query and
HTTP request body without asserting malicious intent. `usvr-agent` raises an
installation warning, while `usar-agent` attempts the same with a misspelled
exception name. Further review of the archives and remaining U detections is
needed before claiming completed sample reviews.

## V batch, partial

All 35 V archives received initial scans. Four previously under-detected
`veriftest1*` archives use setup hooks to post Google Cloud metadata responses
to webhook.site; the existing metadata callback detection now covers them and
all four have verified copies on elrond. A fifth token-targeting version was
already hostile before that extension.

Eleven `vtk-osmesa` versions contain setup commands that attempt to dump the
GitHub Actions runner process, extract values marked secret, and send them along
with environment data to an external endpoint. All eleven now have hostile
findings and verified copies. Execution depends on the required runner,
permissions, and external endpoint.

`voto3` 0.2.0's examined install hook prints a fixed message. `vermillion` 0.3
attempts to run a missing executable, while 0.4 contains the referenced Windows
executable; both read a hard-coded local README path before setup, which can
prevent the hook from being registered. Version 0.5 packages an executable
but does not register that hook. Static analysis of the shared executable
shows a cyclic-XOR wrapper that drops two embedded executables and launches
`ping_tool.exe`. The other extracted program is a Discord-controlled UDP/TCP
traffic bot; the traced wrapper writes it but does not launch it. The packed
bundle now has a hostile trait. Both archives already had hostile ML verdicts
before the trait was added. Other V samples need further review.

`vcdiff-py` 2.1.0 scans benign with a PyArmor finding at crit 4. Its
distribution `__init__.py` and `client.py` are PyArmor wrappers, while the same
archive includes a plaintext source checkout whose setup version is 1.0.0 and
whose VCDIFF decoder and CLI are readable. The distribution metadata says
2.1.0, and its console entry point names `vcdiff.cli`, which is present only in
the source subtree. The included `CLAUDE.md` reads as ordinary development
guidance; no harmful behavior is established from the encrypted modules, so
this review adds no hostile trait.


## W batch, partial

All 24 W archives received initial scans. `wiki-requests` 0.0.3 collects
host and user information, queues it, and sends the queued record to a
hard-coded public TCP endpoint from an installation hook. It now has a hostile
behavior trait and a verified copy on elrond; the archive already had a hostile
ML verdict before this trait. `web3x` 0.1 and 0.2 contain packaging metadata
but no package module. `web3x` 0.3 and both examined `webtraste` versions
contain only directory entries. `wordsdict` contains packaging metadata but
no package module. These initial findings do not complete review of all W
archive members.

## X batch, partial

All 63 X archives received initial scans. Several `xolo*` archives contain
source targeting `.ROBLOSECURITY` cookies with browser-cookie3 and attempting
to post a cookie value to a webhook. The text-based hostile finding now also
covers malformed variants, including `xolocyawkmylds`, `xolodqijhnjgte`,
`xolohnetekcjdz`, `xolomdabxhhrue`, `xolouwdmgbgkvr`, and `xolozamdgbxywf`;
the examined source has a syntax error and its embedded webhook value is not
a valid URL. Those archives already had hostile ML verdicts. The existing
bytecode finding was retained and verified after sharing its cookie marker
with the source rule.

`xiedemo` contains an examined function that prints a fixed message. Static
decompression of `xoloaoqcjnreyc`, `xolofucxlcmyke`, `xolomayflwnfmy`,
`xolommyjlqlhsw`, `xolopfydnuxyfh`, `xolotxobrzatpu`, and
`xoloxygjidhpoo` revealed Roblox
cookie-stealing code behind Hyperion obfuscation and a `Hello world!` marker.
They now have a hostile trait for the obfuscation and package-dependency
combination; their archives already had hostile ML verdicts. Other obfuscated
variants require further analysis. Initial scans do not constitute completed
reviews of all X archive members.


## Y and Z batches, partial

All 12 Y and Z archives received initial scans. Both examined
`youreallydontwantthispackage2131` versions contain setup hooks that fetch
Google Cloud service-account token responses and post them to an ngrok
endpoint. The existing metadata callback detection now covers ngrok too;
both archives already had hostile ML verdicts. The rest still need individual
review despite their initial scan findings.

## Numeric names, partial

All three numeric-name archives received initial scans. `0wneg` is an explicit
package-installation code-execution demonstration that writes a local marker
containing the user and time. It now has a hostile proof-of-concept trait and
a verified copy on elrond; its original archive verdict was benign. The other
two archives had hostile traits at scan time and still need individual review.

## Compromised libraries, partial

All 29 archives in `compromised_lib` received initial scans. `xinference`
2.6.0 and 2.6.2 contain an encoded credential-collection payload launched in
a child Python interpreter; 2.6.1 uses a direct decoder. The existing encoded
credential and archive-upload findings now cover the child-process variants
as well. All three archives already had hostile ML verdicts. Six large archives
(`mistralai`, two `telnyx`, and three `xinference`) emitted a warning that the
member list carried by one result was truncated at 256 entries. This limits
what the scan output alone establishes; individual archive review remains open.

## A batch, partial

The first 60 A archives were rescanned. `ai-labs-snippets-sdk` 0.1.0, 1.1.0,
3.3.0, 3.4.0, and 4.4.0 load a `model.pt` with unrestricted PyTorch
unpickling, but the named model is absent from those collected archives;
the import can only load it if a file is supplied separately. Several sibling
versions contain checkpoints and already have hostile executable-checkpoint
findings. `aiiohttp`, `aiohtttp`, and `aiohtttps` contain packaging metadata but
no package module. `ailzynitro` 1.0 contains no files, and
`aiogram-sever-patch` 3.3.7 contains metadata only. The first 60 scans do not
complete individual review of the other archives or the remaining A batch.

The second group of 60 A archives was rescanned. `artifact-lab-3-package-
a18ff5d9` 1.1.5 prints the complete environment and constructs an encoded
request to an ngrok endpoint, but the inspected function does not send it.
It now has a hostile disclosure-and-request trait and a verified copy on
elrond; its original archive verdict was benign. `aiopbotocore` 0.2.0's
examined install hook prints a fixed message. `aiolrucache` 0.1.0 and 0.1.1
have no observed helper in their collected code; 0.1.1 writes a local install
marker. Version 0.2.0 includes a hostile encoded helper, and 0.3.0 attempts
to import it as a top-level module even though the collected helper is inside
the package. The latter finding now describes an attempt rather than a
proven successful launch. Other A archive members remain under review.

The remaining 69 A archives were rescanned. `asycn` and `asyncoi` contain
packaging metadata but no package module. Of 48 `atlasctf-21-prod-*` archives,
45 setup scripts attempt to read a flag file and post it, while three use a
separate import-time flag-posting module. Three setup scripts use a placeholder
webhook hostname; their configured endpoint is not an established live sink.
All 48 had hostile traits at initial scan. This comparison covers those source
files and is not a complete review of every archive member.

## B batch, partial

All 135 B archives were rescanned; the last 15 had hostile traits. `b10connoisseur` 0.2.0 through 0.5.0
include an import-time upload of environment and cluster information to a
public endpoint and retain hostile findings. In 0.12.0, the examined source
instead exposes a reconnaissance function that records environment and other
findings locally, while separate HTTP probes target cloud metadata services.
An existing co-occurrence rule incorrectly described that as contacting C2;
it is now suspicious and describes only the observed co-occurrence. A new
hostile rule separately binds a process-environment read to an HTTP POST. The
0.12.0 archive still received a hostile ML verdict after the rule correction.
Other versions require individual review.

`builderknower` 0.1.1 and 0.1.2 request a hard-coded URL during installation;
0.1.8 runs a curl callback and tests local writes. These callbacks now have
suspicious findings. The examined 0.1.3–0.1.7 versions do not run those
callbacks, while later versions include encoded environment requests that
already had hostile findings. `bolym` 1.0 contains no files; `botocote`
describes an example typosquat but its examined module only defines an
increment function. Initial scans do not complete the B archive reviews.

## C batch, partial

The 21 C archives that lacked hostile traits in the earlier scan were
rescanned against the current rules. `coloroma` and `colurama` contain
translated Base64 and XOR layers that statically decode to a Linux script
which writes a Python downloader and starts it; the existing carrier rule now
covers both encodings. Both archives already had hostile ML verdicts.
`colorsgradient` 12, 13, and 14 contain no files. `crpto` and `crypo`
contain explicit typosquat warning modules; `cugraph-service-server` 0.0.1 is a dummy module.
`ctftestsowwy`'s examined hooks print a fixed message.

`crytic-compilers` 0.3.7–0.3.9 call an imported `crytic_compile.install`
module from setup, but that module is absent from their collected archives;
the code that would be resolved externally remains unknown. `cryptograohy`
0.7.0 and 0.7.1 instantiate an unpinned `pyprettifier` dependency on import.
The dataset's 0.1.0 dependency is an ordinary emoji utility; 0.1.5 includes
a webhook-reporting decorator, while 0.1.4's converter has a syntax error.
The parent archives do not establish the dependency version resolved. The `convocations` 0.19–0.22
Airflow helper can print a decrypted session password when its debug flag is
enabled; it now has a suspicious disclosure finding. Other functionality
requires further review, and the archive ML verdict alone is not evidence of
a particular behavior.

## D batch, partial

The 11 D archives without hostile traits in the earlier scan were rescanned
against the current rules. `dlocal-cli` 99.0.1 and 99.0.2 now have hostile
install-hook curl findings. In 99.0.1, unquoted ampersands separate the shell
commands, so the curl request includes the hostname but not the later token
assignment. In 99.0.2, the URL is single-quoted and shell substitutions are
literal. The finding descriptions now report the command syntax rather than
asserting that credentials were sent. Version 99.0.0 contains a dummy module;
99.0.3 is a reservation warning.

`detectron2` 0.6 contains no files. `darknegrobbc` contains only dependency
metadata as executable Python. `discodr` and `discrd` contain setup metadata
but no package module. `dfdfdfdfhhh` 1.0.1 and 1.0.2 print fixed messages in
the examined setup and module. `definitely-not-requests` needs further review.
These observations do not complete the D archive reviews.

A `dbt-bytedhouse` setup hook imports a helper that assembles a URL query from
host, user, and working-directory values. The helper uses `urllib.parse` and
`urllib.request` after only `import urllib`; availability of those submodules
depends on prior imports in the runtime. The corresponding generic trait now
describes its co-occurring URL and identity clues without asserting that the
request successfully sent them.
