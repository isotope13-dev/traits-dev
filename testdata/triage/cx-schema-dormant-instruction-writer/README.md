# Dormant installer instruction writer

Reviewed `@cxtms/cx-schema@1.9.278`, SHA-256
`75bf2635677aebe368bb71e98077a888243353c245343c6d0cc431882603dda4`.

The archive contains 257 files: 11 JavaScript files, 159 JSON files, 18 source
maps, nine TypeScript declarations, 40 Markdown documents, 19 YAML templates,
and a GraphQL schema. Atomscan analyzes 238 entries including the archive.
The source maps contain no embedded source payloads. JSON schemas and templates
are declarative application/workflow examples. Bundled agent skills describe
CXTMS scaffolding, schema validation and explicitly requested server commands.
No hostile payload or concealed credential collection was identified.

The installer finds a consumer project, copies schemas into `.cx-schema`, writes
a local validator, and replaces its bundled `.claude/skills` directories. It also
removes four deprecated skills. These automatic agent-skill changes justify
retaining `postinstall-writes-bundled-agent-skill` as suspicious.

The installer defines `setupClaudeMd`, but its only invocation is commented out.
The CLI's separate `init`, `setup-claude`, and update commands can write project
instructions. File proximity alone incorrectly reported the dormant installer
helper as an install-time instruction write. The repaired objective additionally
requires a module-level instruction-target write or a parsed invocation bound
to a local helper naming the instruction surface and writer. Existing neutral
path and write observations remain visible. No package-name exclusion was added.

The CLI loads a local dotenv file, keeps its own OAuth session under
`~/.cxtms/<project>/.session.json`, uses PKCE and a loopback callback listener,
and sends its API token to the configured application server. User-selected file
uploads use server-provided presigned URLs. Log downloads are decompressed as
text. Child processes install/update the CLI or open its login URL. These uses
account for its network, credential, filesystem, encoding and execution traits.
The VS Code setup script only edits YAML schema associations.

## Regression coverage

Run from the repository root:

```sh
python3 testdata/triage/cx-schema-dormant-instruction-writer/check.py
```

The nine controls distinguish active direct/helper writes, renamed helpers,
reordered declarations and conditional calls from dormant helpers, commented
calls, string contents and unrelated writes. Separately, uncommenting the
original sample's helper call restores the suspicious objective.

The helper query covers expression-statement calls at top level, in a top-level
conditional block, or in an ordinary top-level function body. It is lexical
invocation evidence, not a complete runtime reachability analysis. Aliases,
dynamic dispatch, arrow-function helpers and deeper callback nesting are outside
this query. The pre-existing objective also retains its postinstall basename
scope. These limits must not be mistaken for proof that an unmatched installer
is benign.

## Validation and disposition

- Focused cases: 9/9 passed; reactivated original helper matched.
- Final Atomscan: zero hostile traits; one suspicious trait, bundled skill install.
- `make validate`: passed, including hostile 668/668, benign 1478/1478 and
  does-nothing 176/176, plus every additional configured corpus.
- Hopper: moved from incoming to `good/mislabeled-unknown` with `hopper mv`.
- Local archive destination: `/tmp/triage/misplaced-good`.

Raw facts, before/after scan results and validation output are retained locally
under `/tmp/triage/cx-schema-1.9.278/`. This verdict covers the supplied archive;
registry dependencies and future releases were not followed.
