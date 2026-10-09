Version drift triage: FreeBSD VM and Trillian

Judgments: all three supplied artifacts are BENIGN.

FreeBSD VM v1.1.7 and a4d21ef6556fb1cf722059bab3acec1c39c26961:
Fetched https://github.com/vmactions/freebsd-vm.git and compared both
revisions to v1.1.6. All regular archive members match their upstream
Git objects. The release adds runNFSInVM, selects it when sync=nfs, and
skips redundant rsync copyback. The workflow adds an NFS job and narrows
its Ubuntu matrix. Its NAT test sends uname -a;whoami;pwd through SSH to
root@localhost:10022, using the VM's configured NAT mapping. The same
command already exists in v1.1.6's SSHFS and ordinary test jobs. Expected
VM connectivity and environment verification, with output in the CI log;
no added credential export or remote operator command channel.

Trillian v1.3.13:
Fetched v1.3.12.zip and v1.3.13.zip from proxy.golang.org for
module github.com/google/trillian. The supplied v1.3.13 ZIP is identical
to the downloaded archive (SHA256
7590c664eab4cda1161bf88b0e6cec04657370d793793a48bfce96b421563d1a).
The flagged storage/cloudspanner/storage_provider.go only loses its
MapStorage method. The release removes experimental map support across
providers, APIs, deployment, tests and documentation, as its changelog
states. The warning blob and its decode/log code are unchanged.
Its 543 gzip bytes expand to 1608 bytes of warning-sign ASCII art.
warnOnce.Do bounds output to once; Base64 -> bytes.NewReader -> gzip
-> ioutil.ReadAll -> string -> glog.Warningf. LogStorage/AdminStorage
call warn(). The blob is not written, loaded or executed.

Trait decisions and reference audit:
- Move four whoami/pwd command-text atoms and their OR composite out of
  objectives/discovery/system/fingerprint/user into the existing neutral
  process/identity/query leaf. Adjacency does not supply attacker intent.
- Pair atoms/composite remain notable; remove benign-product exclusions
  that merely hid an intrinsically neutral observation. The original
  command-text matchers and language scopes are retained.
- Move USER/HOME query aggregation to os/env/read. Move the user-info
  aggregate to process/identity/query, with an evidence-level description.
- Update the three exact consuming references (Marimo, Oastify, .NET
  stager). The two remaining references to the source directory name are
  Go-profile IDs in a different source YAML file and remain untouched.
- No ancestor directory selectors consume the relocated source rules.
- Drop the inherited T1033 default: the command-pair and environment
  observations alone do not establish attacker reconnaissance.
- Add a notable Go warning-block trait that binds all decode intermediates
  and output, excludes extra statements and executable else branches,
  and permits changed variable names, function names and banner bytes.
  This is logging behavior, not an obfuscation or execution objective.

Controls (all passed):
compressed-warning.go and renamed-warning.go match the warning trait.
warning-and-exec.go, warning-else-exec.go and unrelated-warning.go do not.
second-compressed-literal.go still shows the observed warning behavior;
it does not declare the whole file benign. The archive controls retain
the engine's embedded-gzip finding on payload and unrelated-output
members, including a payload sibling of a warning module.
identity-pair.sh matches the notable command-text observation;
identity-words.sh does not; neither has suspicious or hostile traits.

Engine limitation:
The existing builtin-binary-embedded-base64-gz YAML hook does not remove
this engine-generated finding in the installed build. Tested a narrow
warning-output suppressor, including sibling-payload controls; removed
that ineffective edit rather than claiming suppression. Trillian retains
one distinct suspicious embedded-compressed-data signal, repeated on its
container, source and decoded layer, plus the correct notable decode/log
behavior. It has zero hostile traits. A zero-suspicious gzip result would
require an engine fix; no broad Go-module or filename allowlist was added.

Final scans: both FreeBSD samples have zero suspicious/hostile traits.
Trillian has zero hostile traits and the single distinct engine finding
noted above. Final repository verification is make validate.
