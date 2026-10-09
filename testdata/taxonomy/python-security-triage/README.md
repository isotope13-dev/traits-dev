Python security triage controls

The procfs matcher moves unchanged from the anti-debugger objective to a
neutral path observation. Its regex proves nearby cmdline/stat path formats,
not a process-tree traversal or debugger detection. Severity becomes notable
and the inherited T1622 mapping is removed. The exact anti-analysis consumer
keeps the moved leg; its remaining required debugger evidence is unchanged.
Two ancestor debugger-directory consumers accept native binaries only, so the
Python/pyc path observation cannot affect their accepted population. There are
no ancestor procfs directory consumers of this matcher.

The runtime ignore-prior literal matcher now excludes Python docstrings.
Executable prompt literals stay detected. The MCP exception requires all of:
a server import, virtual-resource declarations, and simulated-read test
declarations. A virtual resource alone must not suppress a runtime prompt.
The exception is referenced only through the existing defensive suppressor.
These controls are static input, never executed.

The Task Manager name observation also moves unchanged into process/info/name;
its exact monitoring-tool consumer is updated. No source or destination
ancestor executable/name selectors consume it. Other rules in the source file
remain in place. Bare powershell.exe references move unchanged into executable
names, with every exact reference updated. Ancestor shell selectors now require
the remaining execution evidence: a name alone must not satisfy execution.
This intentional coverage correction prevents token-only shell convictions;
actual shell-launch observations retain their original scope and matchers.

The LLM composite intentionally suppresses test directories. To check the live
composite, copy these inputs into a directory without test naming first; the
literal atom can also be checked in place.

Simulation and virtual-filesystem wording are documentation claims, not proof
that a file is a test. Their neutral atoms are in documentation/claims so they
do not enter the broad testing-directory suppressors. Only the three-leg
exception belongs to scripted testing, and directory selectors skip exceptions.

Validation evidence: all nine controls passed after copying the inputs outside
test naming. Final local atomscan scans retained the wrapper's two suspicious
anti-analysis findings and emitted zero suspicious or hostile findings for
both wheels. Their SHA-256 values agree with the published PyPI 2.2.2 and 0.6.0
release records. Neither finding originated in a fetched dependency.
