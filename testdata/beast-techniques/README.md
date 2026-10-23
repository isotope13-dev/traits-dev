# Beast technique coverage

Source: https://www.attackiq.com/2026/10/23/beast-ransomware/

The original PE was recovered by Forager from Triage sample
`251001-p1yg5afj8w`. Its SHA-256 is
`4c44ac1eea4bc7f4ea542d611b5658d7ac2729d79abe750da83f1581cd832eaf`;
its size is 82,944 bytes. It was statically analyzed, never executed.
The original bytes and Forager provenance remain outside the traits checkout.

## Evidence and placement

- The bounded string helper at VA `0x407b75` zeroes its index, XORs bytes
  in place, branches backward until its bound, explicitly NUL-terminates,
  and returns the buffer pointer. Its opcode matcher leaves the key and
  length variable. One helper is notable decoding; eight or more such
  helpers establish repeated string concealment. The byte sequence is
  also tested in an inert Linux ELF32 object.
- The WQL query is assembled from XOR-encrypted wide fragments
  `SELECT *`, ` FROM Wi`, and `n32_Shad`, with the remaining characters
  supplied by immediate stores. The three fragments must share a nonzero
  key and reside in `.text`. A native deletion finding additionally requires
  COM creation/proxy imports and the four-argument slot-16 call structure
  used at VA `0x40b367`. Neither fragments nor virtual-call layout alone
  establish deletion. The source equivalent requires an actual
  `DeleteInstance` call near the shadow-copy class reference; comments
  containing method names do not qualify.
- The service routine at VA `0x40abf1` clears EBX, increments it to one,
  and pushes it as the control argument. The call at `0x40abf8` resolves to
  the `ControlService` IAT slot. The rule checks both register continuity
  and the actual import address, rather than treating every ControlService
  reference as a stop operation.
- The hostile file-walker composite requires the shadow-copy deletion
  signature, Recycle Bin removal, ChaCha quarter rounds, file enumeration,
  reads, and writes. Its separate service-impact consumer additionally
  requires the resolved STOP request and process termination. These represent
  encryption/recovery destruction and service/process disruption, respectively.
  Both exceed the documented hostile precision bar (9.1 and 7.8).
- `GetIpNetTable` is a notable Windows neighbor-table capability in the
  admitted `micro-behaviors/network/neighbors` target home. It does not
  itself establish scanning, lateral movement, or encryption of shares.

## Validation

The required final Atomscan directory scan reports **two hostile and two
suspicious traits** on the original sample, satisfying its hostile floor.
The existing rule set initially reported no suspicious or hostile traits.
Neutral findings are not counted toward either floor.

Focused fixtures are in cleave's `tests/fixtures/beast-techniques/`, not the
article's sample directory. `build.py` creates inert PE/ELF fixtures and
source examples. `check.py` checks 22 positive/negative expectations:

- Native WMI deletion with keys 0x55 and 0xA7; query-only and mixed-key negatives.
- C++, C#, Python, and JavaScript deletion; read-only queries, another class,
  and commented method names as controls.
- Direct service STOP calls with different registers; wrong import targets
  and source pause requests as controls.
- Repeated decoder helpers on PE and ELF; one helper and zero-key controls.
- A Python neighbor-table call and its commented equivalent.

All 22 checks passed; none of the focused fixtures fired either hostile
composite. Raw facts, article HTML, 21 extracted preformatted blocks, five
article images, scan reports, and fixture results are retained under the
scratch threat-feed/4202 directory.

## Indicators and limits

`SHA256`, `ENDPOINTS`, and `PURLS` are recorded in the article testdata directory.
There are no package coordinates or package versions in this report.
The actual beacon is `https://iplogger.co/1v1i85.torrent`:
`1v1i85.torrent` is its path component, not a hostname despite the feed's label.
The ransom contacts are `vortexecho@zohomail.eu`, `somran@onionmail.com`, and
Telegram `@somran2024`; both email domains are recorded as contact indicators,
not inferred C2 endpoints. The hash-shaped text in the downloaded filename
is not a verified additional sample hash.

The mutex `BEAST HERE?`, builder placeholders, `.moon` suffix, footer magic,
contact names, and specific beacon are evidence only, not required detections.
The encrypted configuration and unrecovered runtime strings still prevent
precise static coverage of the GUID Run-key write, HTTP header beacon,
attacker key hierarchy, exclusion/kill lists, and per-file encryption schedule.
The native rules cover the observed x86 code forms; no NAS/ESXi binary was
supplied or tested. Two distinct hostile findings are retained rather than
adding overlapping conclusions merely to reach the three-to-five goal.
