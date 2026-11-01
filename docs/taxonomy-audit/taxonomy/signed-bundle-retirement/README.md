# Signed-bundle staging retirement

The final nine rules left legacy signed-bundle staging, and the directory was
removed. The App-V and COM combination with remote-process memory APIs moved to
process injection and retains hostile severity. The NSIS, AutoIt, product-name,
network, service and multi-PE combinations moved to installer, product-reference
and PE-operation profiles. Their descriptions describe the observed combinations
without asserting an Amadey identity, confirmed side-loading or surveillance;
their severities are suspicious. The Elex-specific rules continue to use these
profiles as supporting evidence and retain their own family-level conditions.

The size-bounded CreateRemoteThread reference remains a component in the
memory-operation profile so its historical bounds and consumer behavior are
preserved. All nine match conditions, exclusions, confidence values and size
bounds were checked; exact references and the broad legacy dropper consumer
were updated. The latter's historical weak-evidence audit remains open.
