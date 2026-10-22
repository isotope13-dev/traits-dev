# Second review of cookie bootstraps and modified Mirai ELF

All three supplied SHA-256 values were verified against their bytes. Each was
scanned with atomscan and `cleave facts`, including recovered strings. Review
was static: no specimen, endpoint, command channel or generated mutation was
executed. Findings and classifier outputs were leads rather than proof.

## Cookie scripts: both MALICIOUS

`98067d53be6be867c069b3f95809f014a04c012dafc657f548887b3cb34bbfbd`
(`cookie-grant.sh`) and
`acb00293edac2caedc67c2c96611b58f10352b87089089dc6f6307d75fe6d26c`
(`cookie-without-grant.sh`) are 261-byte shell webshell bootstraps. Reading the
complete straight-line programs establishes their effects:

1. They chmod `/bin/sh`, using 6555 and 0755 respectively. Only 6555 grants
   SUID/SGID; 0755 does not establish privilege escalation.
2. A quoted heredoc writes `/srv/site/.endpoint`. Its PHP body calls
   `passthru(urldecode($_COOKIE['job']))`, with neither authentication nor a
   command allowlist. PHP, rather than the installing shell, later decodes the
   cookie and executes it, returning command output.
3. Another heredoc appends `/etc/httpd.conf`: a Files block enables the PHP
   handler for the hidden file, and an Alias routes `/assets/site.js` to it.
   This combines arbitrary request-driven execution with a concealed endpoint
   behind a static-asset URL, rather than providing ordinary site content.

The scripts do not create the parent directory or reload Apache. Installation
depends on directory existence, write permissions, compatible PHP handling and
configuration reload. Privileged execution additionally depends on ownership,
mount policy and the shell's handling of elevated IDs. Successful deployment
is not established. No package identity/version or authorized test deployment
was supplied. These limits do not negate their intentional backdoor behavior.

All existing script findings accurately describe these operations and remain
unchanged. The no-grant script has one hostile composite covering the command
endpoint and static-URL disguise, plus two suspicious command/handler findings.
Those are overlapping descriptions of one installation chain; a second
independent hostile outcome is not invented to meet a count. The grant script
also has the distinct hostile setuid-shell grant composite.

## ELF: MALICIOUS Mirai-lineage IoT bot

`c9018cee6b41d2664a06abe1a90aaa7d551f20af9abf33a139ec4361eb51fb18`
is a stripped, statically linked x86-64 Linux bot with uClibc. Identification
rests on the actual scanner, task protocol and attack-vector implementation,
rather than its filename or third-party family signatures.

- Entry 0x400194 supplies main 0x405230 to the C runtime. Main initializes the
  string table, overwrites argv[0], sets the process name using prctl, forks,
  creates a session, closes standard descriptors, registers attack vectors at
  0x400740 and launches the scanner at 0x406690.
- The table routines at 0x408410/0x408490 XOR each byte with all four lanes of
  eight words at 0x510920. Their combined key is 0x51. This hides a controller
  domain, shell commands, procfs paths and daemon-name disguises. The credential
  constructor at 0x4064d0 uses byte XOR 0x22 at 0x406556 and its password loop,
  recovering entries including root/xc3511 and default credentials for cameras.
- Main resolves its decoded domain, sets port 61337 and calls connect at
  0x40592f. Receive calls at 0x405b36/0x405b5b/0x405b85 reach recvfrom syscall
  45 through 0x40b44c/0x40b458. A 16-bit framed length is bounded to 1024 bytes;
  0x405ba1 passes the received body to parser 0x400410. That parser extracts a
  big-endian duration, vector, target addresses/masks and options, then invokes
  forked vector dispatch 0x4001c0. This task channel remains intact.
- Scanner 0x406690 constructs raw TCP SYNs to Telnet port 23, traverses random
  targets and connects to responding devices. Its state machine consumes
  Telnet negotiation/prompts, sends decoded username/password pairs at
  0x40758d/0x40763e, and sends shell/BusyBox probe commands. This is a live
  credential-scanning implementation, not merely an embedded password list.
- A connected-UDP loop's send at 0x40336c targets the return stub 0x40b487.
  Existing connected-UDP/flood rules correctly decline that altered loop.
  Other attack paths survive. In particular, vector 0 registers routine
  0x4037a0, which creates AF_INET/SOCK_RAW/IPPROTO_UDP at 0x4038b9, constructs
  IPv4/UDP packets, recalculates checksums and iterates 24-byte target records.
  Send 0x403b22 still reaches syscall 44 via 0x40b494. Branches at 0x403b34 and
  0x403b3d repeat the target traversal and entire sweep. Other vector routines
  also retain send calls; disabling one loop does not disable this program.

Unauthorized credential attempts, operator-controlled attack dispatch and
unbounded packet-generation routines tip the verdict. No authorized lab context,
original registry package/version, installed-host context or runtime success
was established. The decoded controller was not contacted.

## Trait changes and verification

Added one notable raw-UDP capability and one hostile raw-flood-with-credential-
scanner composite. The capability binds socket creation and send calls to the
appropriate syscall wrappers, compares the stored/loaded descriptor and loop
counter slots, and resolves both backward branches. It uses no specimen name,
address, key, size or endpoint. The hostile composite describes co-occurring
raw flood code and credential scanner; it does not claim successful execution.
No existing matcher, severity, exclusion or description was weakened.

Reviewed consumers of the flood capability leaf and UDP objective leaf and
their ancestor selectors. Wraith's UDP-parameter profile needs three findings;
one added raw-flood finding cannot satisfy it. Full rescans confirm no extra
family attribution or unrelated consumer changes.

`check.py` passes 18 static controls, including repaired connected-send coverage,
redirected raw sends/socket calls, wrong descriptor/counter slots, broken back
edges, another protocol, consistent alternative slots, architecture and section
near misses, and three existing benign/network fixtures outside this batch.
Without credentials, the raw-packet capability remains visible and the hostile
composite declines. The existing disabled connected-loop finding stays absent
until that loop's actual send target is repaired.

Rescans preserve every original finding and severity, including the ELF's
33-byte XOR-decoded shell child (not an archive member). Neither script has
members. ELF findings increase from 98 to 100; its child keeps both findings.
Script findings stay at 11 and 12. There are zero detection losses.

Atomscan labels remain HOSTILE (92%) for cookie-grant, BENIGN (33%) for
cookie-without-grant, and HOSTILE (100%) for the ELF. Its raw probability/level
pairs are 0.99/25, 0.99831814/20000 and 0.9997656/0 before; the ELF changes to
0.9998477/0 after. The no-grant script is a classifier miss despite its accurate
hostile webshell finding. No inaccurate or duplicate traits were added to
change that classifier result. The scanner reports feature-spec v18/v19
compatibility warnings; those outputs are recorded as observed.

Marker lines (each at most 72 characters):

```
Cookie webshell: hidden command endpoint and SUID shell grant
Cookie webshell: hidden command endpoint; no SUID grant
Mirai bot: C2 and credential scanner; cover intact raw UDP flood
```

Run the focused controls with the original ELF and a scratch directory:

```
python3 testdata/triage/raw-udp-cookie-review-2026-10-22/check.py SAMPLE --scratch SCRATCH
```

The checked-in JSON records contain control results and complete finding-set
comparisons. Full facts, scans and disassembly are in the session scratch
directory `scratch/acquit-review`.
