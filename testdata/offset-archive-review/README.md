# Calibration, HID and offset-array stage review

The calibration script was interpreted only with a local `curl` stub; the
stub recorded its arguments and made no network requests. The target-side
injected command, HID script, PowerShell sample and downloaded executable
were not executed. Other analysis was static. Facts, original scans,
decoded source, fetch logs, and subsequent scans are under the session scratch
`triage-bad` directory. The checked-in controls generate clearly identified
static derivatives, not recovered malware specimens.

## Judgments

* **calibration-pipeline.sh — BENIGN**, an Edimax-compatible `formWlanMP`
  command-injection proof of concept. One curl invocation authenticates with
  `admin:1234`, defaults to POST through `--data-urlencode`, and sends calibration
  fields to loopback. Single quotes preserve `ateAntenna=|id > /tmp/ate-proof #`
  as a form value; the local shell does not execute that `id` command. A
  vulnerable target may pipe into `id`, redirect its output, and treat the
  remaining command text as a comment. There is no output retrieval, installed
  payload, destructive action, retry/spray loop, or control channel. The bounded
  proof-file operation and loopback target support an assessment PoC judgment.
  Authorization and the actual target service are unknown. A source may label
  this malware because it contains a functioning exploit request.
* **keyboard-stringln.txt — BENIGN**, a DuckyScript HID demonstration.
  `WINDOWS r` opens Run; `STRINGLN` types and submits a PowerShell command.
  The command bypasses execution policy, requests a hidden window and evaluates
  `WebClient.DownloadString` directly. Thus a compatible keyboard interpreter
  would attempt execution; the absent separate `ENTER` is not a safety guard.
  The placeholder `cdn.example.org` destination, exact educational fixture in
  this repository, and published harmless equivalent support the demonstration
  judgment. The URL failed DNS resolution when fetched. No bootstrap contents
  were recovered. Operator authorization and deployment context are unknown;
  external malware labeling plausibly reflects the BadUSB download/eval pattern.
  Retain its suspicious hidden-policy-bypass finding.
* **route-b-method.ps1 — MALICIOUS**, a functional ROMULUS Route-B-style
  reconstruction, not a hash-identified original ROMULUS specimen. Adding
  704123 to each array element produces valid PowerShell. The loop appends
  characters to `$program`, which `ScriptBlock.Create($program).Invoke()` runs.
  The stage compiles Win32 declarations, obtains the console handle, invokes
  `ShowWindow(...,0)`, and moves the console offscreen. It creates a GUID-named
  TEMP directory, downloads a 7z archive and an extractor, and checks 7z magic
  and a minimum-sized MZ image. Those checks establish format, not authenticity.
  It runs passworded extraction hidden and waits; reads an extracted text file
  for the nested password; extracts a second archive; selects the first EXE
  other than the extractor; and starts that EXE hidden. It then attempts to
  remove the environment-specified script path. The inner assignment of
  `$MyInvocation.MyCommand.Path` may replace the previously saved outer path,
  so successful self-deletion is not asserted. Concealment of the complete
  executable workflow plus the exact reported delivery infrastructure tips the
  malicious judgment. No legitimate installation purpose is supplied. The
  archive could not be obtained by URL or published hash through Forager's
  Hopper and research-source fallbacks. Final executable behavior, LegionLoader
  identity, persistence, theft and runtime success are not established.

The primary disclosures corroborate these identities without establishing
runtime success or operator authorization:

* [Edimax researcher disclosure](https://github.com/Erebua/CVE/blob/main/Edimax.md)
* [NVISO harmless HID demonstration](https://blog.nviso.eu/2026/10/16/keystrokes-in-disguise-forensic-analysis-of-a-digispark-hid-device/)
* [Forescout ROMULUS analysis, Route B](https://www.forescout.com/blog/romulus-analysis-of-a-new-multi-payload-clickfix-delivery-platform/)

## Rule changes and limits

* Restore curl's default POST behavior for URL-encoded bodies, with method
  overrides excluded. Existing explicit-POST/body coverage remains supported.
  The resulting HTTP fact also restores the existing calibration-injection and
  output-redirection findings; neither is promoted to hostile.
* Preserve and relocate quoted shell-control observations from process creation
  to `metadata/lang/source/syntax/command`. Matchers, scopes, severity and
  exclusions are unchanged. All explicit consumers now use the new IDs. Broad
  shell-creation consumers should require execution rather than quoted syntax.
* Preserve and relocate typed hidden-window options from process creation to
  `process/argument/option`; update the policy composite. Full HID positive and
  near-miss controls preserve its execution and bypass coverage. The VSCode
  hidden-creation consumer does not overlap these rules' types. The Python
  write/execute consumer continues to require actual hidden-process evidence;
  an unrelated printed option cannot supply that evidence.
* Add eleven notable additive-offset source-token observations. Full decimal
  magnitudes are compared, so the key cancels. No hostname, password, chosen
  variable or filename is required. They cover HTTPS downloading, 7z signature,
  extraction arguments, variable password construction, text/EXE selection,
  process launch, hidden-window options, console APIs and environment-path
  deletion. They assert encoded source syntax, not independent runtime calls.
* Add one hostile concealed-archive workflow composite and two suspicious
  console-control/cleanup composites. Their descriptions state source
  co-occurrence rather than claiming general value-flow proof. The sample's
  actual source-to-launch links were traced manually. The hostile rule requires
  decoding/invocation and all the format/extraction/password/selection/launch
  roles; decoder or hidden-window primitives alone do not convict.
* Preserve the native footer self-copy/launch atom in
  `micro-behaviors/process/deploy/file-exec`, with its original bytes, imports,
  scope and suspicious severity. Update its sole exact objective consumer.
  This separates the mechanism from replication intent and keeps the objective
  leaf within its existing budget. The objective and disk-bomb traits remain
  hostile. Recover the original positive specimen by SHA-256 through Forager;
  all 15 existing static controls retain their expected attack coverage.

The engine caps each YARA pattern at eight matches, making a matcher that
counts every integer unsuitable. The new rules scan from array headers and
compare values at uniform strides. They support compact arrays with 4–9 digit
negative magnitudes, uniform width, and scripts up to 256 KiB. Whitespace,
width transitions and other arithmetic representations can evade these new
observations; the existing generic decoder and obfuscation traits are retained.
No final payload was available to justify further hostile outcomes. The one
hostile workflow plus three suspicious findings is deliberate: additional
hostile counts would duplicate the chain or overstate encoding, hiding, cleanup,
or unseen payload effects.

## Verification

* `atomscan` and `cleave facts` on every original, with full slow scans repeated
  after edits; facts on the decoded stage and an argument-capturing curl stub.
* 21 offset/curl controls: changed keys and variable names, unused decoded data,
  plain text, missing hidden launch/executable/password/extraction roles,
  missing console or cleanup operations, corrupted high digits, default POST,
  method overrides, and retained explicit POST.
* 33 existing HID controls and 10 calibration controls.
* Existing footer replication suite: all 15 controls pass, including renamed
  specimens, low fan-out, broken links, absent rewriting, and unrelated files.
* Quoted shell command positive and ciphertext negative preserve syntax
  detection under the corrected metadata ID.
* The Route-B regression fixture enables YARA explicitly; the validator disables
  it by default, unlike a direct scan. Its bytes equal the supplied sample.
  The detached browser/update benign control keeps zero hostile/suspicious
  limits; its score cap changes 17 to 18 for the preserved metadata syntax
  observation, which is now also an explicit required trait.
* `make validate` is the final action after markers and review artifacts.

See `review.json` for original hashes, before/after counts, classifier output,
ID moves and material losses. No material supported detection was removed.
