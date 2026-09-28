# Encrypted module loaders use the module-load sink

Moved four Node composites out of `dropper/staging/encrypted` into
`dropper/module-load`: the local-file decrypt-and-`require` chain and three
obfuscated dynamic-module loaders. All require dynamic module activation; the
encryption method is evidence for the chain, not its directory axis. Decrypt
and eval rules remain with their interpreter sink, while encrypted material
without an established activation sink stays in staging.

The three obfuscated-loader composites moved as a complete rule file. The
fourth rule was extracted from a mixed JavaScript file, which retains its
generator and decrypt/eval rules. Effective scope, matcher bodies, filters,
confidence, criticality, and attack metadata are unchanged. Three supply-chain
consumers and the evidence comment now use canonical module-load paths.

The encrypted staging leaf drops from **297 to 293 rules** and module-load
grows from **3 to 7**. Soft fixture validation passes all **1,837 cases**;
strict validation continues to report the broader cap and quality debt.
