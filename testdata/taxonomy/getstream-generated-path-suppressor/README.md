# GetStream generated-path suppressor controls

These fixtures keep behavior and neutral-field indicators visible when their source files sit under `src/gen/` or `gen/models/index/`. Those paths occur in the published `@stream-io/node-sdk` package, but a path alone does not establish package identity or provenance and must not suppress unrelated behavior.

The package identity control checks the declared npm name and repository fields against `stream-node-sdk-official`. Those are package metadata claims, not cryptographic publisher verification. The source controls intentionally contain no package manifest, so the identity composite must not match them.

Run with:

```sh
python3 testdata/taxonomy/getstream-generated-path-suppressor/check.py ../cleave/target/release/cleave
```

The checks use synthetic source snippets and Cleave's normal scanner, plus one debug trace for the exception composite (which is not emitted as a finding); they do not fetch packages or execute fixture code.
