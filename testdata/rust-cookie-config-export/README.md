Static controls for the cookie/config TCP transfer, helper-fed API-name lookup,
and allocation-derived remote-thread entry rules. No fixture is compiled or run.

Run `python3 testdata/rust-cookie-config-export/check.py --fixture-parent <scratch>`.
An optional `--sample <rust-source-path>` adds the original source and mutations
removing the VM termination or disconnecting the packet from the socket write.

The checked sample produced 46 passing assertions across 24 controls. The tests
cover renamed bindings, reordered stores, unrelated paths/read results/buffers/
streams, local writes, non-secret targets, comments, shadowed bindings, unrelated
API names, and unrelated/literal thread entry addresses. The bare transfer is
suspicious; the hostile composite additionally requires VM-screening termination,
XOR mapping, and Windows compression references. It does not establish a live C2,
runtime success, or execution of the separate injection routine.

Adding these rules does not suppress any existing finding. The game identity
observations require an embedded player manifest and UI title for the composite;
they do not assert signature validity or a benign deployment. Ancestor game
exclusions were inspected: their independent attack prerequisites do not fire on
the launcher, and before/after scans retained every pre-existing finding.
