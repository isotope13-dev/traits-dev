# Azure AgentBaker release drift

Verdict: BENIGN. The sample is the Go source distribution of Azure AgentBaker,
an AKS node provisioning and image-building tool, at
`v1.0.3-byo-cni.0.20260916220636-2944b6dce46c`.
Its SHA-256 is
`1747c1a59346856ae5125662ea7b237a0c8a5b759e75f912a713d4d9d7fb400a`.
An independently fetched Go proxy ZIP for this exact version has the same hash.

## Decisive earlier-release comparison

Fetched and scanned `v0.20260826.0`: zero suspicious or hostile findings.
Compared its `pkg/agent/utils.go` and `utils_test.go` with the sample. The
production-file diff changes SSH public-key quoting to Base64 and adds the
ten-line `encodePowerShellBase64Literal` helper. The test-file diff adds only
104 lines testing that helper and its SSH-key formatting caller.
The change is upstream [commit 23a4a476, PR #9313](https://github.com/Azure/AgentBaker/commit/23a4a476cfcafd38e8e9296e4b1d76a06dde01aa).
The more recent `v0.20260915.0` already contains these tests and reproduces the
same engine alert; its `cse_helpers.sh` is identical to the supplied sample's.
Against August 26, that shell helper changes service enable/restart ordering,
quoting and Ubuntu 20.04 FIPS kernel mitigation eligibility.

## Execution and data-flow review

`baker.go` registers `GetSshPublicKeysPowerShell` for template expansion.
`getSSHPublicKeysPowerShell` trims each configured public key and calls the
new helper, which Base64-encodes UTF-8 bytes. Its generated PowerShell expression
calls `Convert.FromBase64String`, then `Encoding.UTF8.GetString`.
`kuberneteswindowssetup.ps1.template` puts the resulting strings in `$SSHKeys`
and passes them to `Install-OpenSSH`. In `staging/cse/windows/configfunc.ps1`,
that routine writes them using `Add-Content` to
`C:\ProgramData\ssh\administrators_authorized_keys` and sets its ACL.
The decoded values are data; they are never passed to `Invoke-Expression` or
an encoded-command launcher. This change prevents interpolation of quotes and
PowerShell subexpressions in key comments.

`cleave facts` recovers the Base64-decoded test strings, including
`ssh-rsa AAAAB3 user@host`, `ssh-rsa AAAAB3 ;$(cmd)` and a key containing U+2019.
The unit tests compare generated expressions and decode them back to the
original key text. The scanner instead treats even-length UTF-8 key bytes as
UTF-16LE and labels the resulting Unicode gibberish an encoded PowerShell
command. For example, offset `0xf82e` contains an expected string expression
for the first key, not a `-EncodedCommand` invocation.

The two supplied GitHub asset URLs were fetched, scanned and inspected.
They implement GitHub browser UI behavior: search result requests and DOM
updates, code navigation, user-triggered blob downloads and clipboard copying.
They are assets of the linked GitHub HTML page, not AgentBaker runtime imports.
Both have zero suspicious or hostile findings.

## Trait correction and verification

Removed `foreground-interactive-shell` and its alternative from
`cli-operator-console`. Its raw-text regex matched arbitrary `*Shell()` names,
including `getSSHPublicKeysPowerShell()` inside a test error message. Neither
that spelling nor a call to an unknown function establishes shell execution,
interactivity, foreground operation or C2 infrastructure. Existing process
API traits remain responsible for actual execution observations.

Run `python3 testdata/version-drift-agentbaker/check.py`. All three controls pass:
a Shell-named function plus banner/API context cannot substitute for session
evidence; the remaining three console conditions still match; and an actual
`exec.Command` call retains its notable process-creation finding.

The archive rescan removes the retired YAML finding and reports zero hostile
IDs and one distinct suspicious ID: `binary/embedded/base64-powershell`.
That false positive is generated in Cleave's `embedded_code_detector.rs`,
including several artificial decoded layers. It has no YAML override hook.
No YAML shadow, sample allowlist or severity demotion was added. Correcting it
requires the engine to distinguish UTF-8 data decoding from UTF-16LE command
decoding; the remaining alert is not evidence of malicious sample behavior.
