# Container namespace taxonomy audit

The namespace leaf mixed namespace operations with container-runtime identity,
network-interface names, and host-root path operations. Those facts now live
with their own technique or characteristic: OCI/CRI/CNI and runtime names under
container metadata pending a capability-placement re-audit, interface names under
`micro-behaviors/network/interface`, and
host-root `chroot` behavior under filesystem root operations. Unsupported,
unused roll-ups were retired. Linux namespace operations remain in the
platform-neutral `micro-behaviors/os/container/namespace` leaf; their Linux or
Unix applicability is carried by rule scope. Static syscall predicates share
that leaf in `direct-syscall.yaml` because the matcher evidence is syscall
specific, not a separate taxonomy technique.

Rules classify the best-supported program characteristic from static evidence;
they need not prove runtime execution. The boundary is behavioral: a rule
belongs here when it characterizes creating, entering, or configuring an
operating-system namespace. A string identifying a container runtime or
OCI/CNI interface can be evidence of a related runtime/network capability;
its placement must follow that probable capability, not its string matcher.
A `veth` or bridge-interface name supports probable network-interface
interaction, without narrowing it to namespace creation. A `chroot` into a host path changes filesystem root and belongs with
root-directory operations even when a container-escape composite consumes it.
Platform names may appear when they name the technique itself, but do not add
generic platform levels beneath shared techniques.

The intermediate network-string parent had YAML rules above its `interface/`
child, violating the strict leaf-only contract. Five port-reference and
service-table rules currently share `metadata/file/string/network/port/`; their
six consumer rules retain seven exact references. This port placement is
provisional: it must be re-audited by probable capability under the clarified
taxonomy contract. The interface indicators have already moved to the existing
capability leaf. See the
[`network-port-leaf-mapping.json`](network-port-leaf-mapping.json) ledger and
the matching placement rows in `TAXONOMY.md`.

The mapping ledger and consumer audit are in
[`namespace-cleanup-mapping.json`](namespace-cleanup-mapping.json) and
[`namespace-cleanup-consumer-audit.json`](namespace-cleanup-consumer-audit.json).
The inert controls under `controls/namespace-cleanup/` verify interface
capability indicators, namespace operations, and host-root changes. The
network-interface leaf had 94 rules at this checkpoint; the subsequent
[wireless audit](INTERFACE-WIRELESS.md) reduces it to 80 through subject-correct
relocation. The placement correction was not a size-cap exemption.
The audit also found two malformed references in an unrelated .NET ransomware
composite: its references included YAML filenames as though they were taxonomy
path segments. Those were corrected to the canonical rule IDs so validation
could load the catalog.

After the capability-placement correction, all 16 focused verdicts and all
1,826 fixture cases pass under `validate --soft`; `git diff --check` is clean.
There are still 167 oversized directories, including the 94-rule interface
leaf, and other strict-validation debts. No mixed parent/leaf nodes are reported.

The interface move expands five existing directory references by the two
indicators. Four consumers are scoped to Windows PE/DLL files; the incoming
rules retain their original Unix source/ELF scope. The fifth,
`objectives/exfiltration/messaging/webhook::webhook-with-system-data-host-2`,
can now use interface-name evidence alongside its required nearby IP-field
evidence. That is an intentional expansion of capability evidence, not a claim
that the reference alone establishes collection or transmission. Matcher bodies,
criticality, and effective file/platform scopes of both atoms are unchanged.
