# Second conviction review: companion and PowerShell cradles

No family attribution or threat-feed conviction is inferred from filenames,
registry origin, ML scores, or the literal word `malware` in a hostname.

## Identifications and judgments

- `95f4270f7cea24165674f752e41aac46f02c74197c5b71f4dd758c8efb206f0d`:
  MALICIOUS, a direct-action DOS companion virus. Its executable body is 43
  bytes; the remaining 85 bytes are zero padding. It finds the first name
  compatible with `*.E*`, changes its DTA extension to `COM`, creates the
  previously absent same-name twin, and writes its own entry image to it.
  DOS command resolution can select the COM twin ahead of the original EXE.
  It does not append to, overwrite, or run the original EXE, enumerate further
  results, install a resident interrupt hook, or access the network.
- `83de8a7eb152c2a294d83c1c31621f54039f53be0c0920e896216b5316135643`:
  MALICIOUS marker retained at **suspicious-only confidence**. This readable
  seven-line ZIP/REST stager downloads an archive to TEMP, extracts it, invokes
  an EXE there, and pipes a separate REST response into Invoke-Expression.
  The policy-bypassed child only invokes Expand-Archive; the remote evaluation
  is in the parent. The Defender exclusion comes last. Neither ordering nor
  child-argument data flow supports the former hostile claims.
- `1bf9493e22468ec6f6b8b5838ee501218ea739e1bc447b3ed40e79e84fc8384e`:
  MALICIOUS marker retained at **suspicious-only confidence**. Same archive
  staging, executable launch and REST evaluation, followed by process-scoped
  policy bypass and a Defender exclusion. The bypass follows the first two
  execution sites, so it is not proof that either ran under the changed policy.
  No PowerShell child process is created in this variant.

Both scripts use a reserved `.test` hostname and stop on errors. They resemble
small demonstrations, and neither includes the fetched payload. These details
limit the conviction: staging plus Defender exclusion warrants suspicion but
not a hostile payload claim, family identity, real C2, theft or persistence.
A reserved hostname alone is not a benign exemption: hosts files and private
resolvers can supply it. The traits retain observable capabilities and only
co-occurrence-based suspicious conclusions. No endpoint was fetched or sample
executed against the real filesystem/network.

## Inspection and corrections

`atomscan` and `cleave facts` were run on every original. All PowerShell source
and its parsed calls/literals were inspected; no encoded layer is present.
Rizin 16-bit disassembly and full byte inspection covered the entire COM.
Binwalk is not installed in this environment. Unicorn emulation with fake DOS
services confirms HOST.EXE -> HOST.COM and the 43-byte own-image write; failed
search/create paths do not write. This emulation writes no host files.

- Removed the false embedded-child-eval composite and its unsupported hostile
  Defender consumer. Removed the generic hostile fileless-eval composite:
  unrelated bypass/embedded-command co-occurrence is not attack admission.
- Added a suspicious Defender-exclusion/parsed-REST-evaluation co-occurrence
  rule in the exclusion leaf; it makes no ordering claim. Extended the existing
  process-bypass rule to recognize actual pipeline evaluation as well as the
  nested spelling. The archive/exclusion rule remains suspicious.
- Tightened the abbreviated CLI flag to require a token boundary, so the
  middle of Set-ExecutionPolicy is not mislabeled as a launch flag.
- Moved the firing PowerShell HTTP observations into the existing admitted
  client-call catalog; moved artifact-suffix URL references into URL paths.
  Preserved their original scope, matchers and exclusions; fixed all exact
  consumers and local references. The one live legacy-catalog selector now
  names a group preserving its original membership. The two parent `http/lib`
  selectors are Python-only and cannot select these PowerShell-scoped facts.
  Parent download selectors intentionally stop treating the relocated URL
  literals themselves as downloads; an actual transfer remains visible.
- Removed ingress-transfer mappings from neutral archive extraction, renamed
  the Defender preference call atom so it does not imply an exclusion argument,
  and moved the entry-COM-extension observation to file creation.
- Added a complete entry-pointer/create/write observation for the padded DOS
  form. The transfer count and trailing padding are not fingerprint gates.
  Companion admission now requires COM extension evidence; arbitrary DTA
  extension patching and arbitrary buffers no longer establish infection.
  Infection admission references that stronger conclusion.

## Controls

Run `verify.py --samples-root <samples> --scratch-root <scratch>` here. It stages
fixtures outside test-path suppressors. Eleven cases cover both originals and the shared-CWD companion variant,
a differently encoded/padded DOS variant, non-image and non-COM near misses,
a quoted REST pipeline, an ordinary staging script, a Defender-only script,
and an unrelated archive-extraction child. Six benign controls have zero
suspicious and zero hostile findings. The DOS originals/variant have three
hostile findings. PowerShell originals have zero hostile and two/three
suspicious findings. The existing stager-conviction-review twelve-case suite
also passes. The modified hostile companion composite exceeds the 3.5 precision authoring floor.

Final atomscan verification uses slow mode, no automatic updates, and
`--follow=none`. Judgment markers are beside the originals outside the traits
repository; their <=72-character lines are included verbatim in the commit body.

The first full validation exposed the byte-identical PowerShell fixture's
obsolete hostile floor and a missed 44-byte DOS variant. The fixture now
requires both suspicious exclusion contexts, with a corresponding score floor.
Rizin and mocked DOS emulation of the 44-byte variant confirm that its shared
CWD/INC-DH dispatcher restores DX=0100h and writes its own image after creating
HOST.com. Under the emulated name it writes 93 bytes including padding; it then
attempts an invalid empty filename and terminates through DOS service zero.
A separate complete dispatcher observation preserves that existing hostile
coverage without admitting arbitrary extension-patched data-buffer writes.
