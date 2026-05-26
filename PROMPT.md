Cleave flagged this benign sample as a possible threat. Tune the YAML traits to suppress the false positive without weakening real-threat detection.

**File**: /data/samples/good/harvest/github/Devolutions-UniGetUI-3.3.7-source.tar.gz
**Extracted to**: /tmp/cyclotron-be8a883c/extract/b6bbc5

**Current findings**:
```

### /data/samples/good/harvest/github/Devolutions-UniGetUI-3.3.7-source.tar.gz!!UniGetUI-3.3.7/src/UniGetUI/Assets/Utilities/uninstall_scoop.cmd (batch, score 40)
S objectives/evasion/security-bypass/policy/execution::bypass-execution-policy powershell -ExecutionPolicy ByPa  # objectives/evasion/security-bypass/policy/execution/

### /data/samples/good/harvest/github/Devolutions-UniGetUI-3.3.7-source.tar.gz!!UniGetUI-3.3.7/src/UniGetUI/Assets/Utilities/install_scoop.cmd (batch, score 40)
S objectives/evasion/security-bypass/policy/execution::bypass-execution-policy %pwsh% -ExecutionPolicy ByPass  # objectives/evasion/security-bypass/policy/execution/

### /data/samples/good/harvest/github/Devolutions-UniGetUI-3.3.7-source.tar.gz!!UniGetUI-3.3.7/src/UniGetUI.PackageEngine.Managers.Chocolatey/choco-cli/redirects/RefreshEnv.cmd (batch, score 40)
S objectives/command-and-control/dropper/execution/batch::temp-tmp-stage-path %TEMP%\_envset.tmp  # objectives/command-and-control/dropper/execution/batch/
```

If actually malicious, `touch /data/samples/good/harvest/github/._Devolutions-UniGetUI-3.3.7-source.tar.gz.BAD` and exit.

Targets: ≤1 suspicious finding, 0 hostile/misleading findings, 0 validation errors. Keep `notable+` findings that help differential analysis (network, exec, persistence, privileges, obfuscation); suppress what every program fires.

Read RULES.md and TAXONOMY.md before editing. Tighten expressions (`size_min`, `section`, `for`, `not`, `count_min`, composites) before dropping criticality. Relocate misleading traits rather than weakening them. Fix, don't delete — preserve detection intent. In YAML, reference traits as `<subdir>` or `<subdir>::trait_id`; never include the base filename.

Validate with `make validate`. When done, write a single line (≤100 chars) describing WHICH trait you loosened and WHY to `/tmp/cyclotron-be8a883c/worktrees/worker-02/_RATIONALE.txt`.
