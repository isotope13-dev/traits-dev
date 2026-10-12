# traits-dev

Private development and staging tree for the YAML/YARA rules consumed by
[cleave](https://github.com/atomdrift-project/cleave). Reviewed releases are
published to the public
[Atomdrift traits repository](https://github.com/atomdrift-project/traits).

End users should install or update traits through cleave rather than cloning
this staging repository:

```bash
cleave update-rules
cleave version
```

## Validation

```bash
make validate                  # reuse unchanged successful validation
make validate-uncached         # fresh fixture analysis
make validate-profile          # uncached phase, fixture, and rule timings
make validate-profile SLOW_RULE_MS=100
```

The performance targets are under 2 seconds cached and under 60 seconds
uncached. Use a release cleave build; the Makefile prefers the sibling
checkout's `target/release/cleave`. Rebuild after changing cleave or its
dependencies so validation exercises the updated engine.

The full-validation cache verifies rule and fixture contents, expectations,
directory layout, validation settings, and the linked engine's identity on
every run. Changes invalidate it even when file sizes and timestamps stay
the same. Failed or interrupted runs do not populate it. Profiling bypasses
this cache and reports aggregate trait costs, including Tree-sitter queries;
`--verbose` also computes a separate, expensive fixture-overlap diagnostic.
