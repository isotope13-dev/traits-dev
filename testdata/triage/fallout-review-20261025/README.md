# Reasoned sample review

The original bytes were reviewed statically. Atomscan local/slow scans and
full cleave facts were collected for all three originals; the principal
Craft bundles also received individual facts extraction. Source call paths,
arguments, local-variable relationships, decoded-string views, templates and
archive members were inspected. No specimen or downloaded assembly was run.
The scanner reports source-flow limitations and incomplete embedded-source
recovery on some Craft members; relevant source paths were traced manually.
Static review does not establish runtime success or complete interprocedural
value flow through the absent native runtime.
Reports and fetch provenance remain in the session scratch/fallout-review
directory; review.json records hashes, counts and per-member differences.

## Judgments

* **craft-native-0.0.341.tgz: BENIGN.** TypeScript SDK and CLI for building
  native desktop/mobile apps. A forager fetch of pkg:npm/craft-native@0.0.341
  from registry.npmjs.org produced the identical SHA-256
  bfc61a102d378e2c6be271f13a7d03c1a78377d941be764d786865551ab55aaf.
  Its 216 tar entries include readable ESM/CommonJS SDK bundles, platform
  templates, project examples and development workflows; the scanner reports
  224 units, including extracted layers. Package entry points agree with the
  README and implementation. There is no runtime dependency or install hook.
  The CLI launches user-selected native binaries and build/package tools.
  Browser/native bridges expose documented filesystem, process, crypto,
  camera/location and storage APIs. Base64 helpers convert bridge/file data;
  they do not conceal an executable stage. Cleanup targets owned temporary
  directories, with PID, age and keep-marker checks. The configured updater
  checks SHA-256, supports public-key signature verification, and checks macOS
  bundle trust before clearing quarantine and replacing the application.
  These documented capabilities and matching registry bytes favor benign
  tooling. The invoking application, configuration and native binary are not
  supplied; no claim about their future use is made.
* **3-different-destination.cs: MALICIOUS.** Cleartext CloudTasks agent reads
  DRIVE_TOKEN, polls Graph drive children every 30 seconds and dispatches
  hexadecimal filename suffixes. One branch downloads assembly bytes, calls
  Assembly.Load/GetType/GetMethod/Invoke and PUTs the returned result. Another
  downloads a local pathname, reads that exact file and PUTs its bytes.
  The write branch uses undefined `other[1]`, so the standalone source cannot
  compile as provided and does not establish a task-selected write target.
  Existing write-task detections correctly decline. Arbitrary remote code
  tasking and remotely selected file theft tip the judgment despite the broken
  branch; successful deployment is not established.
* **existing-local-backup.cs: MALICIOUS.** Same assembly tasking/result channel.
  The upload reads a fixed user-selected-backup.bin pathname, ignoring the
  downloaded path; it is a file upload, not remotely selected file theft.
  Its separate line-task branch binds task[0] to the fetched Graph item and
  task[1] to the local write destination. Unrestricted remote code dispatch
  and arbitrary remote file writes tip the judgment. An authorized agent or
  research use is possible, but neither authorization nor such a deployment
  is established. No malware family, bootkit, shell implementation, persistence,
  credential theft or behavior of the absent assemblies is inferred.

## Detection changes and preservation

* Bound adjacent C# File.ReadAllBytes and PutAsync(ByteArrayContent) statements
  now expose local-file upload at notable severity. Both originals gain this
  capability. A different body variable, intervening reassignment, or another
  HTTP verb does not match. It adds no exfiltration or remote-path claim.
* WebExtension request/remove/contains require a chrome/browser namespace.
  Craft's `craft.permissions.request(permission)` targets native mobile
  permissions and does not establish extension authority. The former rule
  falsely labeled index.js, index.cjs and mobile.js, plus their archive parent.
  The two sibling rules had the same unsupported receiver assumption.
  Native-object controls and inert strings/comments no longer match; browser,
  chrome and window.browser operations remain detected. The independently
  fetched [MDN permissions example](https://github.com/mdn/webextensions-examples/blob/main/permissions/page.js)
  retains both request and remove detections. Its actual call symbols also
  matched the old regex. There are no YAML consumers of these three exact IDs
  or their WebExtension directory selector.
* The upload-handler identifier matcher moves unchanged to
  metadata/lang/source/naming/interface. Its description and notable severity remain;
  an identifier alone establishes neither a file nor a transfer. Exact-ID and
  source-name ancestor consumers were searched; none selects this observation.
  Upload ancestor consumers were inspected. They must obtain transfer evidence
  from real operations, rather than a handleUpload/processUpload identifier.
  Both declaration-only and network-handler controls retain the metadata fact.
  Existing cloud attack and benign controls retain every original finding.
  This correct placement keeps the upload leaf within its 100-rule budget.

## Results and checks

Hostile/suspicious counts are **0/0 to 0/0**, **4/3 to 4/3**, and **6/3 to 6/3**,
respectively. Every Craft member remains at 0 hostile and 0 suspicious. The
only removed sample finding is the demonstrated native-permission false
positive; neither C# sample loses a detection or severity. All other findings
across the 224 Craft units are preserved. The malicious sources' supported
outcomes are already covered: assembly tasking/results, selected-file theft
in the first variant, and task-selected file deployment in the second. New
hostile rules would duplicate these outcomes or invent absent behavior.

The classifier remains HOSTILE for all three: probabilities are unchanged at
1.0, 0.99995 and 0.9999492. Craft is a remaining classifier false positive;
inaccurate rules were not added to influence its score. Atomscan warns that
the loaded v18 feature specification predates expected v21, limiting conclusions
about model awareness of current features. This is separate from rule validation.

`python3 testdata/triage/fallout-review-20261025/check.py <fetched-MDN-page.js>`
passed 18 relationship, native/browser permission and outside-batch cloud-task
controls. Original before/final reports were compared by ID and criticality.
The older cloud-task-review-20261025/check.py has an unrelated stale expectation
for assembly-load-variable-argument versus the current assembly-load-buffer;
none of this review's rules changes that overload observation. The other
cloud-task assertions pass. Final acceptance uses `make validate`.
