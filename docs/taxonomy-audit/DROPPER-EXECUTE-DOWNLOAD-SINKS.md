# Downloaded payload activation follows its sink

The WinHTTP rule `unsigned-winhttp-remote-thread-stager` requires a WinHTTP
download flow, remote-process memory operations, and remote-thread creation.
Those required primitives describe process injection, so the composite moved
from `dropper/delivery/execute-download` to the canonical
`dropper/process-inject/` leaf.

Its matcher conditions, `for: [pe, dll]`, Windows platform scope, maximum file
size, suppressors, criticality, and tags are retained. The former file default
`attack: T1105` was already overridden by the rule's explicit combined ATT&CK
tags; `mbc: E1105` is now explicit to retain the effective tag. No consumer
references the old rule ID. The `execute-download` directory falls from 219 to
218 rules. Other WinHTTP rules remain in the directory until each activation
sink and its evidence relationship are reviewed.
