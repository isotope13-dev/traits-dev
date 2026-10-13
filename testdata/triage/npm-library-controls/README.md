# npm library triage controls

The three supplied archives contain regular files only, with matching supplied
SHA-256 digests. PPOM-validator manages signed Blockaid data, local cache
metadata, a caller-supplied PPOM provider and rate-limited Ethereum RPC calls.
Smarturl parses and formats caller-provided URLs. Smartstream adapts Node/Web
streams, handles backpressure and reads caller-selected files. Encoded content
is TypeScript source maps. No hostile code, install-time payload, credential
harvesting or exfiltration was found. Flow limitations were addressed by
reviewing shipped source and compiled JavaScript, including decoded maps.

Corrections:
- Equality checks do not assign globalThis properties. Move the assignment
  matcher from process/interpreter/wasm to data/property/assign, describing
  its properties without implying Node origins or WASM. The sole exact
  consumer go-wasm-host-execution references the new ID.
- MetaMask-owned library repositories do not identify the wallet. Narrow the
  wallet repository atom to the extension/mobile projects.
- Erased generic typeof import type arguments do not load modules. Check the
  enclosing context while retaining runtime imports.
- Generic stream buffer writes do not establish process I/O. Move the atom
  unchanged to data/buffer/transfer. The PowerShell streamed-MSI consumer uses the new ID;
  broad selectors were audited. Update the existing transfer comment.

Placement checks separately considered facility and required operation:
property assignment has no execution sink; generic buffer transfer has no
process receiver. Existing destination leaves admit both observations.

Controls pair assignments with comparisons, runtime imports with erased type
imports, buffer writes with message writes, and wallet with library repositories.

MetaMask scope-name observations move to metadata/package/name/identity.
The core-library exception now requires both scoped name and core repository;
a namespace alone cannot prove core-library identity or suppress behavior.

Positive assignment, runtime import, buffer-write and wallet-repository controls
match their corrected traits; comparison, type-only import, message-write and
library-repository controls do not. PPOM manifest retains name metadata but
does not satisfy the core-library exception.
