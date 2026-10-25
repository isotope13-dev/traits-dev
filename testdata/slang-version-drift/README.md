Slang master source archive: BENIGN
=================================

Sample SHA-256: `2c0fcbfb4630f6d7e18d6c818c05aac3b955d91bbaea29979e640d2a4110c0e1`.
The gzip tar archive's PAX comment identifies upstream revision
`52e29ab43bf46f70f043297ea2aff02d1ace1988`, described by Git as
`v2026.20-56-g52e29ab4`. Its expanded version file says
`v2026.20-56-g52e29ab43bf`.

Provenance and decisive diff
---------------------------

Fetched [v2025.23.2](https://codeload.github.com/shader-slang/slang/tar.gz/refs/tags/v2025.23.2)
with forager and cloned upstream history. That earlier source release has
zero hostile or suspicious findings with the original rules.
[Commit e694c6c5](https://github.com/shader-slang/slang/commit/e694c6c56aa665b77d2d7a034a3dd3a9854f31bc),
"Enable Claude Code workflow on Windows self-hosted runners with GPU (#9204)",
introduces the flagged PowerShell command while switching from Ubuntu to
Windows and forwarding the installed executable to the Claude action.
This is an explicit CI platform-support change, not a substituted dependency
or a concealed payload.

Compared every regular file and symlink against the upstream revision's Git
blob IDs: 13,486 match exactly. The only differing member,
`cmake/slang_git_version`, is the expected Git archive `export-subst`
expansion declared by `.gitattributes`. The flagged workflow itself matches
upstream byte for byte.

Execution trace
---------------

The Windows-only setup step evaluates `https://claude.ai/install.ps1` through
`irm | iex`, searches expected install directories for `claude.exe`, writes
the discovered executable path to `GITHUB_OUTPUT`, and adds its directory to
`GITHUB_PATH`. The local composite action forwards that path to
`anthropics/claude-code-action@v1`. The adjacent jq setup downloads a pinned
jqlang release and writes cmd/bash quoting wrappers; its escaped strings are
wrapper construction, not encoded payload concealment. Other workflow steps
check out source, initialize submodules, build Slang and run the assistant.

The [vendor quickstart](https://code.claude.com/docs/en/quickstart) documents
the exact Windows install pipeline. Fetched its current script with forager:
it chooses x64/ARM64, downloads the version manifest and executable from
`downloads.claude.ai`, checks the manifest's SHA-256, runs `claude install`,
then removes the temporary download. This current response corroborates the
installer purpose; it is not a reconstruction of the historical response.
No downloaded program was executed during this review. Actual runner state
and historical network responses are unavailable. The source provenance,
ordinary platform-support diff, and explicit executable handoff tip the
judgment to BENIGN; the verdict does not depend on a clean scan.

Trait correction and consumer audit
----------------------------------

`objectives/command-and-control/dropper/script-eval/response-pipeline::ps-iwr-pipeline-eval`
required only the existing notable
`micro-behaviors/process/deploy/script-eval::powershell-web-response-piped-eval-text`
plus file-scoped exclusions. It added no evidence of C2, malicious delivery,
concealment or unauthorized execution. Consolidated that redundant suspicious
objective alias into the existing neutral capability without changing the
capability's matcher, scope, severity or exclusions. Network acquisition and
evaluation remain visible at notable severity, including for plain HTTP.

Audited exact and ancestor-directory consumers. Repointed the public-code
pipeline, Defender-exclusion and Chocolatey scheduled-stage consumers to the
canonical trait. Added it to the plugin consumer's existing OR list so its
directory selector does not lose the moved observation. The other ancestor
consumer, `windows-embedded-security-hosts-sinkhole`, is PE/DLL-only and could
not consume the removed VBS/PowerShell/batch rule; no change was needed.
These consumers retain their additional attack context. They no longer
inherit the removed alias's unrelated vendor-file exemptions: merely
mentioning an official installer must not suppress another malicious chain.

Verification
------------

Ran atomscan and cleave facts on the original archive, and facts on the
workflow and its extracted PowerShell setup. Saved all reports, decoded-fact
data, forager provenance, Git diffs, blob comparison and control comparisons
under the session scratch directory `version-drift/`.

Before/after rescans of all archive members differ only by removal of the
redundant alias at the setup script, workflow and inherited archive root.
Unique hostile/suspicious counts: **0/1 -> 0/0**. Including all inherited
report occurrences: **0/3 -> 0/0**. The original notable pipeline finding is
unchanged at all three levels. No accurate capability or hostile detection
was lost. Earlier v2025.23.2 has **0/0** with the original rules.

Atomscan v18.18 / engine 2.13.0 stays ML-benign (`lvl=-1`, `conf=0`):
archive maximum probability **0.8275946 -> 0.79637325**, workflow
**0.29743290 -> 0.03200537**, extracted PowerShell
**0.82759458 -> 0.22886546**. Raw probabilities do not override its calibrated
verdict. No remaining rule/classifier disagreement with BENIGN. The engine
reports its older feature-spec/model revision and source-analysis limits in
some other members; the relevant setup pipeline was recovered and manually
traced despite those limits.

Pre/post scans of existing controls from `drop-exec/`,
`stranded-member-controls/` and `powershell-official-installer-url/` retain
every hostile finding, including hidden policy-bypassed execution, Empire
cradle behavior and Defender exclusions. Only the redundant suspicious alias
is lost on pipeline controls. The existing 21-case good-pool suite and both
official-installer fixtures pass with updated canonical-trait expectations.

Run `python3 testdata/slang-version-drift/check.py` for 13 controls covering
official installation, ordinary HTTP evaluation, download without evaluation,
Defender tampering, public hosted staging, the existing hidden-execution
fixtures, plugin context, Chocolatey scheduling, and official-URL mentions
beside an unrelated attack. Fixtures are copied/generated outside testdata
and scanned without execution. All 13 pass.
