# Pinned skill release triage controls

The supplied archive hashes were verified and every extracted member compared
against its ZIP entry. Both releases are benign on the inspected bytes:

- ClawVault installer 0.2.13 creates a venv, installs GitHub main, configures a
  loopback inspection proxy, edits the existing gateway unit, and exposes local
  dashboard operations. It explicitly disables TLS validation. Dangerous
  commands and injection strings are detector test inputs. Cloud audit is
  disabled in its default configuration. The remote GitHub dependency is not
  bundled and this judgment does not attest future bytes installed from main.
- Meta-Skill Generator 1.0.0 scans skill documents, builds local JSON/vector
  indexes, requests model-generated source, tests it, and writes generated
  skills. Local exec and temporary-file subprocess tests provide no security
  isolation. The Docker path requests a read-only container with networking
  disabled and no new privileges, but has implementation defects and falls
  back to local testing. No secret collection or unauthorized send was found.

Both archive scans have zero suspicious and zero hostile YAML findings. Source
flow analysis reports limitations for the large manager/tester functions;
manual inspection covers those paths. No source decoding layers were found.

## Matcher and placement corrections

Systemctl text and escaped user-service fragments moved from persistence to
service control; the persistence consumer references that neutral group.
Python pip installation and upgrade composites moved from shell execution to
package installation. The upgrade argv observation lives under argument
options. Literal interpreter/script subprocess creation moved from local-exec
to subprocess, while an argv-list observation moved to argument/file.

The weaker DEVNULL proximity matcher was retired in favor of the canonical
matcher requiring stdout/stderr assignment to subprocess.DEVNULL. All exact
consumers were updated. This intentionally rejects unrelated nearby mentions.
The broad HTTP result-string matcher was consolidated into the existing JSON
result/output-field matcher, whose type scope now includes scripts/source.
HTTP consumers now describe proximity rather than an unproven data flow.

Generated-source identifiers and TimeoutExpired references moved to source
metadata. Agent directory and SKILL.md references moved from IPC to their path
homes; the latter no longer accepts mere agent/skill prose. Consumers were
updated. Generic ancestor references were reviewed: these observations add no
IPC, shell, persistence or interpreter-evaluation claim on their own.

TLS policy text is excluded from the authentication-variable matcher and a
literal unit-environment TLS-disable observation was added. setup.py whitespace
now requires the setup filename observation; its generic metric lives in file
line metadata. A generate function name no longer claims payload generation.
Broad exception/file-open proximity no longer claims append or error flow, and
ordinary exception handlers no longer inherit an obfuscation ATT&CK mapping.
SSH filename clusters say references, not enumeration; connect_ex no longer
claims nonblocking behavior. Illustrative pipeline wording says text.

OpenClaw target references no longer produce an observability-product identity.
PyYAML identity now requires its reader-module path and implementation header,
rather than a dependency error message. These identities have no external
suppression consumers. No archive filename or version-specific allowlist was
introduced.

cases.json records positive and near-miss controls, including both-claim and
same-content/different-filename controls. Analyze the fixtures with the current
traits and compare their IDs with matched/not_matched. The supplied archives
were also rescanned using atomscan with automatic rule updates disabled.

All 16 positive/near-miss controls passed on the final rules. Both final
atomscan runs completed successfully with only notable-or-lower findings.
