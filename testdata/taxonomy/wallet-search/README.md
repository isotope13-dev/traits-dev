# Filename search and export-source controls

Run `python3 scripts/check-wallet-search-routing.py` from the repository root.
Fixtures are copied outside the test-data tree and scanned, never executed.

Controls cover wallet globs versus generic `id.json` search, local search versus
Telegram send, PowerShell traversal versus a bare mask, extension predicates,
application-bundle discovery, a retained traversal-dependent consumer, and the
JSON filter underlying a retired hostile wrapper.

The two Mach-O fixtures contain only constant strings. Rebuild each with:

```
clang --target=x86_64-apple-darwin -c id-json.macho.c -o id-json.macho
clang --target=x86_64-apple-darwin -c generic-options.macho.c -o generic-options.macho
```

`id-json.macho` matched the old wallet selector and mixed Telegram exporter.
It must now match the generic file exporter and not the wallet selector/exporter.
The shell wallet-export control must match the wallet branch instead. The
bundle-credential control checks that moving a filename predicate does not lose
its useful traversal evidence in an existing acquisition classifier.
