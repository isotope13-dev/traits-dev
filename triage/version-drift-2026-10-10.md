# Version drift triage, 2026-10-10

All three submitted artifacts are BENIGN. The reported alerts are false
positives, not evidence of compromise between releases. Samples were inspected
as source and configuration; none of the flagged members needs native
instruction disassembly. Downloaded archives were unpacked without running code.
Full scans, archive facts, and relevant member facts are retained in the task's
scratch/version-drift directory outside the traits checkout.

## Wolfi py3.13-pip-base 26.2.1-r4

SHA256: 8aa3908a2983ae6c673e7203a8f303e71dc3ac34acea54de772de020edb60e76

Fetched 26.2.1-r3 from
https://packages.wolfi.dev/os/x86_64/py3.13-pip-base-26.2.1-r3.apk.
All installed payload files are byte-identical. Only .PKGINFO, .melange.yaml,
and the versioned SPDX SBOM differ: epoch, build time, provenance, and build
prerequisites. There is no new executable behavior to explain either alert.
Fetched PyPI pip 26.2.1, 26.2, 26.1.1 and 25.2 source archives as additional
controls. pkg_resources is identical across these releases. run_script reads
the caller's globals, preserves __name__, resets the namespace, and executes
an explicitly requested installed distribution script. issue_warning walks
frames to choose the warning's stack level. This is reflection, not hidden
payload evidence. The AUTHORS line contains U+200B in a contributor name;
it was already present in pip 26.2. Distlib util and compat implement ordinary
package installation, subprocess, HTTP, archive, and compatibility utilities.
The newer vendored msgpack/urllib3 revisions relative to PyPI are also present
unchanged in r3; they cannot explain an r3-to-r4 compromise.

Fix: relocate caller-global access to micro-behaviors/metaprogramming/reflection
at notable, update both pickle consumers, and recognize conventional AUTHORS
and CONTRIBUTORS documents through the existing documentation exclusion.

## Harn hostlib / VM 0.10.162

SHA256: ab4798c29f3d281ba6264329e42d1be5b261693d0dbc1bfc6a6a08ab75956abb

Fetched harn-hostlib and harn-vm 0.10.161 and harn-vm 0.10.162 from crates.io.
The host library supplies opt-in code intelligence and deterministic tools to
an agent VM. Its build.rs enumerates shipped schema pairs and generates an
include_str! catalog in OUT_DIR. The only hostlib data difference besides
release metadata is a grammar-fitness receipt. conformance.rs is unchanged:
its osascript argv uses Foundation's atomic write API on workspace/atomic.txt
to check that a sandbox permits an intended operation. It is not credential
access. VM security/mod.rs is unchanged: EXFIL is a constant identifier for
phrases that raise a prompt-injection risk score, not an EXFIL command string.
The fork bomb occurs in unchanged policy-rejection tests, including
command_policy/tests/preflight.rs; Command::new elsewhere does not execute
that literal. The catastrophic policy returns a denial reason for a detected
fork bomb. The VM source diff adds optional-path normalization, read-only
preparation annotations, and create_new .gitignore handling for runtime output.
No new beacon, exfiltration path, or disruptive command handoff was introduced.

Fix: require string-content boundaries for the EXFIL prefix, relocate the
osascript language-selection argv to notable process/argument/option, and
replace file-wide fork-bomb/API co-occurrence with a Rust AST query binding
Command::new(bash/sh), arg(-c), and the bomb argument in one call chain.
The query is whitespace independent; it no longer makes claims about arbitrary
Python/C execution or binary co-occurrence without demonstrated handoff.

## Piotr1215 dotfiles

SHA256: 0206b3e3d598273f6d309c679d32100d43efd7ccdbdce953c2f77904cc5427a3

Fetched the GitHub repository and compared all 787 regular files at
32e2b532d467 with the submitted Go module ZIP: zero content differences.
Its immediate parent, 3a1fe772, has the same service. The submitted commit
only adds EVE preview display adaptation and associated tests. To identify
what actually introduced the alerting service, fetched and archived the
parent of 37c241c7152e01f2d5e1b48894f9e7e54890971b and inspected that
commit's diff: it adds the dashboard unit and updates an existing tmux RAG
monitor session to fold in backend latency monitoring. The earlier session
already ran scripts under ~/.claude and inspected its injection event log.
The unit names an ordinary Python file below .claude/scripts, configures
restart and default.target, and documents loopback/Tailscale listening.
It is ordinary user-service configuration, not a concealed payload filename.
The Python dashboard implementation is not shipped in this dotfiles archive;
this judgment covers the supplied configuration, not unseen external code.

Fix: the hidden-argument matcher must end at a hidden filename component;
a dot-directory ancestor followed by an ordinary script no longer qualifies.
The positive hidden-file service control still matches both existing alerts.

## Placement and controls

Caller-global reflection and interpreter language options are neutral
capabilities. Their consumers now reference the neutral IDs; old atomic IDs
have been removed. Exact references and ancestor selectors were audited;
no blanket reflection or option selectors consume these additions. AUTHORS
is documentation-location evidence, not a program identity allowlist.
The remaining attack matchers require their claimed content or relationship.
Nine focused source/configuration controls cover real handoff vs policy text,
EXFIL literal vs Rust identifier, author text, frame reflection, JXA argv,
ordinary dot-directory scripts, and hidden payload basenames. Expectations
are recorded in testdata/expectations.toml. Source controls are scanned only.

Final atomscan runs with CLEAVE_TRAITS_DIR pointing at this checkout found
zero suspicious or hostile traits for all three supplied artifacts and their
scanned dependencies (829, 506, and 559 analysis records respectively).

A separate forced slow scan of harn-vm 0.10.162 also has zero suspicious
or hostile traits (2267 analysis records); this verifies the dependency
that the balanced parent scan skipped. binwalk was not installed despite the
environment description; source/configuration inspection and archive diffs
provided the relevant behavior evidence.
