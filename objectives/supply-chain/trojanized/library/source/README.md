# Trojanized library source traits

Rules in this directory must establish both sides of trojanization from their
matchers:

1. The source belongs to, or preserves identifiable provenance from, a
   known-good library or framework.
2. The same source contains behavior that contradicts that upstream identity
   and indicates an injected backdoor or harmful modification.

Being source code found inside a package archive is not sufficient. Generic
loaders, persistence, command-and-control, credential theft, exfiltration,
obfuscation, and impact behaviors belong in their canonical objective
directories. A wholly malicious package belongs under
`objectives/supply-chain/hidden-payload/` only when its matcher also establishes
package-specific delivery or concealment.
