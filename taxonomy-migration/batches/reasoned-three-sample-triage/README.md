# First reasoned review: three samples

Identity and judgments

- 5e7482c795628bf8aaf243c2aab4b15ba53e91e7cf9acee7748b7fa732bb2fe6:
  Website Status Indicator 1.7.1, benign. Its options page is the only loader
  of SweetAlert2 11.10.1. No content scripts, web-accessible resources, debugger,
  devtools page, or scripting permission exists. The regional routine requires
  a Russian ccTLD, impossible on this extension origin. Preserve dormant code
  as one suspicious finding. Standalone library and scripting-enabled archive
  remain hostile. This is a declaration-based context rule, not a package whitelist.
- 3b7042a152baac78ca4df5bea49ce21e36088071efaa1c7c902db854cba41814:
  Urelas native implant, malicious. Disassembly shows complemented message
  bodies, length plus AS101 framing, Winsock send/receive, HGDraw helper staging,
  executable installation, and a legacy HKCU Windows Run value write. The
  collector's multi-family filename is not evidence. Sandbox corroboration:
  https://tria.ge/261011-dc2n4ac18j identifies Urelas with score 10/10.
- f388bf3f6148c565548d67a7faf65e73a5b1ae06dc51f17a4f3295dbed201a27:
  @intutic/sync-daemon 2.4.0, benign. Governance sync and optional redacted
  config upload use caller-configured authenticated endpoints; local execution
  installs/removes declared hooks and protection. Dangerous command strings
  are policy patterns. Neither package.json nor its barrel import has install
  execution hooks. Both @intutic/mcp-governance-proxy and @intutic/shared-types
  2.4.0 were fetched, inspected, fact-extracted and scanned independently before
  and after changes; each has zero hostile and suspicious findings.

Placement and coverage review

- All four old data/encode/pecompact atoms and the packer composite move to
  well-known/dual-use/packaging/pecompact. PECompact identity is a legitimate
  packer fingerprint, not an encoding operation or attacker intent. PEC2NO
  and PEC2TO are header markers, not section names, and become notable.
  The banner explicitly accepts any section. A 512-byte minimum admits real
  packed PE images while excluding tiny fragments. Other matchers and scopes survive.
  Every YAML consumer was updated. The W^X section observation drops its
  obsolete packer exclusion: packer identity cannot make actual permissions
  false. This intentionally preserves the structural fact and downstream
  neutral API profiles, separately from placement-only migration. No external non-YAML mapping referenced
  the removed IDs. Directory selectors remain any-identity checks: the added
  packer composite requires existing identity atoms and adds no new truth case.
- Two PECompact network-stager composites are deleted: overlapping sections,
  socket APIs and an IP cannot establish staging or C2. Their file had only
  those two rules. The raw-disk unsigned-writable-entry profile retains its conditions and
  exclusions as a notable capability in disk/raw; remove attack mappings and
  unsupported payload/C2 wording. The generic socket profile is retired after
  auditing socket/connect at its 100-rule limit: its client, IP, and entry-point
  facts already have distinct observations and the composite adds no supported
  operation beyond them. This removes redundancy rather than shuffling rules
  around the directory limit. The other rule in
  their former source stays unchanged. No consumers reference the retired IDs.
- n8n HTTP Request node text moves unchanged from exfiltration to HTTP client
  library capability. A named secret-key assignment moves unchanged from AES
  to key/representation. GNU rm's no-preserve-root flag moves unchanged from
  destruction to directory deletion; remove its unsupported attack mapping.
  Explicit and local consumers now reference the new canonical IDs.
- SweetAlert2 identity records code presence as notable. The duplicate archive
  conviction is removed; no consumers reference it. Actual behavior remains
  hostile unless the archive declares extension-only execution surfaces, when
  it downgrades once to suspicious. Remote audio no longer excludes identity
  alone. Generic target="body" is no longer described as an HTML form target:
  require a form-named receiver and describe that limited evidence.
- Added Urelas byte signatures wildcard relocations, not sample addresses or C2
  hosts. AS101 is the family wire-protocol discriminator. Helper filenames are
  corroborating any-legs. The protocol and installation composites are separate
  observed claims, not generic packed-network-client convictions.

Admission and distinguishing claims

The current validator admits dual-use/packaging and crypto/key/representation;
all other destinations already exist. The reviewed sparse fs/disk partition
explicitly admits raw. PECompact's subject is named packer identity; a generic
high-entropy PE is its counterexample. Disk/raw records raw-device read APIs together with
Winsock, IP, and entry-point observations; these component claims intentionally
overlap with the composed profile. Key/representation records named key targets,
not AES use. HTTP client library records a request node, not credential theft.
These placements were checked against both the tier litmus and neighboring
operation/identity homes. Neutral co-occurrence cannot supply attack intent.

Fixtures and results

`focused-results.json` records eight passing positive/negative source fixtures.
`scan-results.json` records original samples, isolated fetched dependencies,
standalone/exposed library controls, and the modified protocol near miss.
The modified native near miss replaces AS101 with AS999 without changing size:
zero Urelas hostile matches, structural suspicious observations preserved.
The archive control adds scripting permission to the original manifest and
repackages identical member bytes: regional sabotage remains hostile.
PECompact controls derive from the identified native sample, without execution:
positive writes PEC2NO/PEC2TO at raw 0x200, the documented SEH bytes at raw 0x400,
and PECompact at raw 0x450; negative removes its PEC2NO header token. The positive
matches all four relocated atoms and their composite; negative matches none.
Detailed outputs are recorded alongside this note.
The raw-disk networking profile also has a near miss replacing only its matched
IP-literal spans with same-length non-IP bytes; the profile stops matching.
The physical-drive read profile description now states API/path co-occurrence,
rather than implying the matcher binds a disk handle to ReadFile. Original native scan supplies
positive raw-disk/network co-occurrence; its negative protocol control demonstrates
that those capabilities alone do not create Urelas intent. Family composite
precision scores are 11.1 and 11.0 (no strong inflation warning).
