# Shell installer staging review

Six shell composites moved from legacy installer staging. Their predicate legs,
formats, scopes, exclusions, and confidence values were retained; references and
the Xamloader directory-wide consumer were updated to include their new IDs.

* Compiling a hidden output and the variant that also deletes an installer
  artifact now live under `objectives/evasion/file-hiding/dotfile-create`.
  Neither says the binary was executed or calls itself a dropper.
* The GitHub archive source build-install combinations moved to
  `micro-behaviors/os/package-manager/install`: their evidence supports a build
  and install workflow, without requiring hostile intent.
* Tar extraction and local command execution with a dynamic-DNS reference moved
  to `objectives/execution/payload/file-exec/command/shell`. The likely staged
  local execution is retained as suspicious, while the description does not
  claim a demonstrated download from that host.
* Archive download and extraction paired with a bracketed process lookup moved
  to `metadata/file/profile/archive`. The lookup alone does not prove a process
  was installed or impersonated a kernel thread. The composite is suspicious
  rather than hostile and no longer carries the unsupported masquerade claim.

Unsubstantiated inherited ingress-transfer labels were removed; the individual
source traits remain available to consumers for their own analysis.
