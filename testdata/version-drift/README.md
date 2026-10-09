Version comparison triage
=========================

Both supplied archives are BENIGN.

LISA: @codyswann/lisa 4.72.5, GitHub main source archive.
Fetched https://codeload.github.com/CodySwannGT/lisa/tar.gz/refs/tags/v4.72.4
(tag commit 5ba6829f393917b85a78cd5c4ae95f052aadd0fc).
The complete tree comparison shows a guardrail parser enhancement: resolve
proven script-directory bindings when following execute/source/stdin operands,
strip heredocs, bound recursion and inspection, and add boundary/parity tests.
Generated copies of the guard and plugin version manifests change together.
The three flagged evidence files are byte-identical in the previous release.
Saved hooks point to Codex's own LISA hooks. inject-rules.sh reads local eager
Markdown and emits additionalContext; install-pkgs.sh handles dependencies;
setup-jira-cli.sh configures Jira. The transcript records BLOCK decisions,
including the disk-wipe command; it is not executable shell input.
The claimed version differential therefore does not reproduce in the flagged
content: an earlier clean scan is not proof these strings are newly introduced.

setproctitle: Python C extension 1.1.10, official source distribution.
Fetched PyPI 1.1.9 metadata and its files.pythonhosted.org source tarball.
Full source diff: setuptools fallback to distutils, packaging/manifest changes,
remove redundant linux/prctl.h include, Python 3 Linux platform handling,
formatting/copyright changes. test_environ's env invocation is unchanged.
It runs only when the test requests a child interpreter, modifies TEST_SETENV
and PATH, reads inherited environment locally and asserts preservation after
setproctitle relocates the argv/environment memory area. No new exfiltration.

Trait changes
-------------

* Move the existing env-command matcher from an import-time objective into
  micro-behaviors/os/env/enumerate::python-env-command-reference, notable.
  Preserve its matcher and update its only consumer. Its prior matcher proved
  neither module-level execution nor unauthorized collection. The new leaf is
  the taxonomy's documented environment-enumeration operation; its nearest
  sibling read addresses individual variables. Future environment-to-HTTP
  composites continue to reference the neutral observation.
* Move the broad SessionStart directory observation into agent-hook IPC.
  The existing objective now additionally requires the platform-mandated
  .claude/settings.json or settings.local.json path. Saved JSON declarations
  remain notable; Codex-owned hooks are not foreign Claude settings.
* Include a BLOCK verdict in dd-zero evidence and reject only that match.
  An unrelated BLOCK line must not suppress an executable wipe elsewhere.

Controls
--------

Copy fixtures to a neutral scratch directory before running: testdata paths
activate existing test-harness suppressors. Active and saved hook JSON have
identical contents and differ only in platform-consumed placement. Test active,
blocked and mixed dd lines. env-helper.py and env-init.py must both produce the
neutral notable reference, while env-mention.py must not. A new leaf's positive
and near-miss fixtures distinguish enumeration from an unrelated env literal.

Full-archive review also found a generated test program quoting
process.env.GH_TOKEN in npm-update-hook-provider.test.ts. The test asserts
result.token is null, validating removal of the gateway token. Its source
literal supports a neutral env expression reference, not credential access:
move env-gh-token to os/env/vcs::node-gh-token-code-literal, preserve the
matcher without objective-specific suppressors, and update its group consumer.
The parsed member matcher remains separate and identifies actual source access.

The literal's generic source-control grouping and GitLab/Bitbucket literal
siblings also move to os/env/vcs, notable, with their exception contexts and
all five objective consumers updated. This avoids reclassifying the moved
neutral literal as suspicious through its old generic grouping composite.
No source-control read alone establishes credential theft.

Verification: python3 testdata/version-drift/check.py passes all nine controls.
Full initial revised LISA scan reviewed 9,844 entries; its sole residual
suspicious observation was the generated GH_TOKEN test literal. Targeted
rescan after migrating that observation and its grouping has zero suspicious
or hostile findings. setproctitle's revised full scan reviewed 25 entries
with zero suspicious or hostile findings. Final atomscan runs cover both
original archive paths after all rule changes.
