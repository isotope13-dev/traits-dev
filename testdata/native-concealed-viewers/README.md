Native concealed viewer and Python bootstrap review, 2026-10-24.

All three samples are MALICIOUS. No Windows sample was executed. Analysis used
complete atomscan reports, cleave facts, Rizin disassembly, PE exception/unwind
function boundaries, and Capstone instruction/argument tracing. The complete
working evidence is in the session scratch directory
/usr/local/var/cyclotron/tmp.noindex/cyclotron-28a4cdc2/scratch/matrix-quartz-triage.
Baseline reports and full original facts are in scratch/bad-analysis/0–2.*.

Sample evidence:

* 59d051af0c4d (matrixhub.exe): unsigned Zig native Python bootstrap. Entry
  0x401011 reconstructs strings by XOR with a separate 16-byte key. It queries
  the processor registry name, disk capacity, uptime, RAM and CPU count; selected
  environments branch to UD2 at 0x4023e1. It constructs eth_call JSON for a
  Polygon contract through several RPC endpoints, parses the ABI/hex response
  to obtain the downstream host, and falls back to an encoded domain. The host
  is passed into 0x402494. That routine builds a per-user Microsoft/Windows
  runtime directory; retrieves Python 3.12.7's embeddable ZIP, enables import
  site, stages get-pip and requirements, sets PYTHONDONTWRITEBYTECODE, and stages
  Python/native-extension files from the selected host. Its execution path
  reaches CreateProcessW at 0x405e2d. These are a concealed payload deployment
  chain, not an ordinary visible Python installer. The fallback domain was
  sltnnt.ru; forager retrieval of the requirements URL failed DNS lookup.
  No downloaded final payload or successful execution is claimed.
* 2fab76025c50: unsigned TemplateForge 8.1.2830.64, declaring Crest Tools,
  with a genuine Rust egui document UI and an unrelated concealed protocol
  module. 0x1300805d4 is a progressing additive byte decoder, seed F5, step F7,
  with inlined UTF-8 output. Config at 0x13007dba3 decodes updatercheck.com,
  cheerquery.com and babslothdrew.com. Command/result handling records com,
  success, ec, dur, st1/st2, truncation flags and errors; the serialized index
  key is stored elsewhere, not contiguous with those fields. 0x13008289f builds
  gzip output, applies feedback XOR plus seed/index rotations, and produces
  encoded reports for the HTTP module. Profile response dispatcher
  0x130092a8a invokes 0x13008c4e7 at 0x130094038. The profile handler constructs
  --user-data-dir arguments, invokes taskkill.exe /PID /F, handles profile
  files, and relaunches via CreateProcessW with CREATE_NO_WINDOW at 0x13008f54a.
  This covert remote-control module is unrelated to document rendering.
* 9226e7565fcc: unsigned QuartzLine 2.0.7031.0, declaring Guoying Communication
  Technology Co, with a real Rust Slint document UI and the same encoded profile
  control protocol. Config at 0x140011ce5 calls the decoder at 0x14002e7bc
  (seed E9, step F3), recovering westbeavers.com. Its profile schema reorders
  bprFile into rFilebp. Required offset-control fields, response JSON decoding,
  the gzip/feedback-XOR/rotation codec, taskkill construction at 0x140017284,
  no-window process configuration and browser-profile restart paths are present.
  Command-result fields from the TemplateForge/older build are absent: do not
  infer that build's arbitrary-command handler for this binary.

The two viewers are consistent with CLOUDHAZE's independent document viewer
and browser-control modules. This is supported by reverse-engineered code,
not version names or scanner labels. Deployment/installer context is missing.
The submitted files have no Authenticode certificate table; a declared company
is not a signer and cannot establish signature trust. Standard Rust sysinfo
ReadProcessMemory/VirtualQueryEx wrappers are not evidence of credential dumping.

Primary corroboration:
https://rogueauthority.org/quartzline-signed-pdf-viewer-zenith-backdoor
https://expel.com/blog/quartzline-a-working-pdf-viewer-with-a-backdoor-inside/

An independent original CLOUDHAZE PE,
7f1db334fd3302cf98dd4afddf6f90e98e2a496fe7e86bf1832b89d02f3d73c3,
was fetched with forager into scratch, with .forage.json provenance and matching
SHA-256. All four baseline hostile findings survive (one moves from beacon to
HTTP channel); the new browser-control channel brings its count to five.
Its published signature/deployment behavior is not attributed to these
unsigned submissions.

Rule changes and accuracy boundaries:

* XOR rules previously enumerated only the first eight matches of a common
  decoder because Cleave sets YARA-X max_matches_per_pattern to eight. Added
  length buckets retain the original matcher and recover late candidates;
  a separate 32-byte candidate handles the crowded Windows-path bucket.
  Ciphertext, RIP-relative source/key and decoded bytes are still verified.
  This does not remove the engine's per-pattern eight-occurrence limitation:
  many identical-length decoders can still require engine support.
* The additive decoder accepts both out-of-line and inline UTF-8 append forms.
  The command-result schema no longer requires a separately stored index key;
  the profile schema accepts both observed orders. No original alternative
  is removed.
* Field-sequence rules move from data/format/json to serialize/schema-object.
  All exact consumers are updated. Recursive ancestor-selector audit found
  no affected general directory consumers. The blockchain observation is
  renamed to rendezvous, the supported result, rather than claiming activation
  from its conjunction alone.
* Encoded command reports move from beacon/network/http to
  channel/http/transport: nothing in the required matcher proves repetition.
  Process execution keeps T1106; an imported CreateProcess API plus protocol
  context does not itself prove the cmd.exe interpreter sub-technique.
* The new browser-control channel requires two decoder/codec implementations,
  both profile schemas, HTTP-client context, forced-PID termination arguments,
  and the Chromium profile flag. The profile-manipulation consumer accepts
  that channel as well as the original command-reporting channel.
* Schema capacity was audited: no identical effective rules existed. Two GUID
  field observations each had direct/property atoms and a transparent OR
  composite. Only the union IDs had external consumers. Each union is now one
  YARA atom preserving both original regex predicates; duplicate component
  observations are consolidated, with no union detection or scope loss.
  Unrelated mailbox-collection ATT&CK mapping is removed from these neutral
  standalone fields. No global budget was raised or overflow directory added.

Run python3 testdata/native-concealed-viewers/check.py. Eighteen controls cover
both decoder implementations, a changed addition operation, both profile field
orders, every omitted channel role, no feedback codec, late XOR candidates,
plaintext near misses, and direct/property GUID positives and near misses.
Generated PEs have an immediate-return entry; signature snippets are unreachable.
They are static matcher controls, not simulated execution evidence.

Coverage and classifier results (H = hostile, S = suspicious):

| Sample | Before H/S | After H/S | ML probability before/after |
|---|---:|---:|---:|
| MatrixHub | 0/1 | 1/2 | .894212 / .991230 |
| TemplateForge | 0/0 | 4/0 | .639187 / .954808 |
| QuartzLine | 0/0 | 2/0 | .538915 / .908354 |

No original accurate detection is lost, allowing documented ID relocation.
All input archive-member lists are empty; there are no extracted archive
members whose detections are omitted. The original signatures and four hostile
detections in the independent CLOUDHAZE control are retained.

The live atomscan classifier verdict remains BENIGN for all three inputs before
and after. Its v18.18 ML export has lvl=-1/conf=0, despite the increased
probabilities and hostile static rules. The final live tiny renders confirm
"scan benign" for MatrixHub (.991), TemplateForge (.955), and QuartzLine (.908).
Its warning says the feature spec predates expected v21. This remains a
classifier disagreement; no rule is inflated to force a model threshold.

MatrixHub and QuartzLine remain below the 3–5 hostile-trait goal. MatrixHub's
runtime staging and activation are reverse-engineered, but the generalizable
required evidence currently supports one concealed rendezvous objective and
two suspicious analysis/concealment objectives. An additional file-execution
matcher binding the assembled runtime paths to CreateProcess arguments was
not established. The unavailable final stage prevents payload-specific claims.
QuartzLine's server-controlled profile file transfer is not given a separate
exfiltration finding: the candidate field-token conjunction did not establish
a source-to-send binding. Its exact requested files and mutations are remotely
selected. There is no evidence to add credential theft, persistence, or an
arbitrary command handler just to increase the hostile count.
