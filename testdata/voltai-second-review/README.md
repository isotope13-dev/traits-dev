These controls distinguish installer instructions, browser regex matching,
React context creation, documentation filenames, and PDF object lookups from
execution, token-format patterns, Node VM calls, and global COM GetObject.

Check benign.js for absence of:
- micro-behaviors/process/create/shell/bridge::node-named-child-process-exec-call
- micro-behaviors/process/interpreter/vm::vm-createContext-call
- micro-behaviors/data/format/credentials::npm-token-format-scan-regex
- micro-behaviors/process/script/wsh::wsh-getobject-variable-argument
- objectives/supply-chain/hidden-payload/extensions/vscode::vscode-obfuscated-curl-shell-exec

Check execution.js for the first four capabilities above, plus:
- micro-behaviors/communications/http/download/curl::curl-pipe-shell-in-js-exec

The executing installer control is neutral. The extension objective additionally
requires VS Code activation/integration and strong code concealment. Its measured
precision is 6.6. A bare IP endpoint, process API import, or installer suggestion
supplies no attack admission. Their ordinary capability findings remain available.

Relocations preserve their scopes and update exact and local references. A
String.prototype assignment is consolidated with the existing property-assignment
trait; computed response calls and command-handler references belong to dispatch,
not payload activation or remote tasking. Decoded fragments have synthetic names,
so they cannot establish a physical filename-extension mismatch.

execFile with explicit shell -c and a curl pipeline is also a neutral execution
control. Malicious corpus regressions retain hostile coverage for cache-marker-gated delivery (precision 7.3) and persistent terminal shell-argument
replacement (precision 6.4), without treating installer instructions as execution.
