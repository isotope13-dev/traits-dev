# VBScript function-result evaluation

`Execute CStr(value)` is a dynamic evaluation capability. Its matcher alone
does not establish obfuscation or a loader, so it moves from
`objectives/execution/interpreter/vbscript/loader::execute-function-call` to
`micro-behaviors/process/interpreter/eval/direct::vbs-execute-function-call`
at notable severity. The required decoding techniques stay in its objective
consumers. All three exact YAML consumers and both fixture expectations follow
the move. No YAML ancestor-directory consumers select the original leaf.

The matcher and file/platform scope are preserved. Separately, a match-level
exclusion removes SQL `EXECUTE AS (` syntax: AS is a SQL execution-context
keyword rather than a VBScript function name. This works independently of
filename or package identity and retains real function-result evaluation.

Evidence: npm @dbml/core 3.14.1, SHA-256
`ebce6ad17c849b07084b8237f4b60d9288e9d9b77594edb092a9ac7704c36c3f`.
Fetched @dbml/core 3.14.0 from the npm registry and compared all 162 members.
No files were added or removed; 160 were byte-identical, including
`TSqlParser.g4` (SHA-256
`635512a5e54b4729935873a8a6fdd62a60fc47d1e0897842da926fc008e980cf`).
The other changes are manifest version/dependency/gitHead updates and Oracle
exporter DEFAULT-clause ordering. At grammar line 2081, the old matcher
misread `EXECUTE AS (SELF | user_name = STRING | OWNER) COMMA?` as a
VBScript call. Parser.parseMSSQLToJSONv2 feeds ANTLR tokens into tsql_file(),
then MssqlASTGen constructs a schema model; there is no SQL execution sink.

Controls cover uppercase/lowercase SQL grammar, ordinary VBScript evaluation,
existing Firebird SQL documentation, and the division-table VBScript loader.
The loader must retain both hostile decoding-and-evaluation composites.

The direct-evaluation leaf was at its 100-rule budget. Its
`html-entity-more-command` atom only observed encoded token text, not
evaluation. It moves with the same matcher and scope to
`metadata/file/encoding::html-entity-more-token`, at notable severity for
encoding presence. Its sole exact consumer, `network-share-file-piped-to-cmd`,
now references that metadata fact. Generic evaluation selectors should not
count an isolated encoded word as execution. The remaining direct-evaluation
leaf stays at 100; no directory or budget expansion is needed.

The full scan also mislabeled hundreds of standalone grammar-production names
as a wordlist. An ANTLR grammar-declaration observation now excludes that
wordlist interpretation, without relying on `.g4` filenames.

The changed @dbml/parse dependency was fetched in both versions too. Its only
code change, after parsing and consistent identifier-renaming comparison, is
the bundled numeric conversion helper replacing `-1 / 0` with a negated
Infinity variable; the identifier correspondence is bijective. Both bundles
parse without errors; manifests only update version and gitHead. No new
networking, execution, collection or persistence behavior was added.
