Relay compiler `0.0.0-master-c45f540f` is BENIGN. The submitted archive's
SHA-256 is `4aeb79253a69af02f4abef974cb61b85590ae9c9f6241775374c3b2666e26dec`;
its SHA-1 and SHA-512 match npm's distribution metadata. Forager recovered
`relay-compiler@0.0.0-master-646d94f3`, published immediately before it on
2020-11-11. All 256 member names are identical. The only changed members are
`package.json`, `index.js`, `bin/relay-compiler`, `relay-compiler.js`, and
`relay-compiler.min.js`; every changed byte is a release-version substitution,
including the matching `relay-runtime` dependency pin. Normalizing that version
makes all executable members identical. Under the current rules the preceding
release reproduces the same alerts, contrary to the queue's earlier clean scan.

The compiler reads GraphQL sources and schema, transforms its IR, and writes
query artifacts and generated types. It hashes file contents and queries,
can watch source changes through Watchman, and exposes Mercurial add/forget
operations. Its `getLanguagePlugin` and `getPersistQueryFunction` use
`eval('require')` to obtain Node's require at runtime without webpack rewriting
it. Configuration chooses the module path; eval evaluates the constant
`require`, not that module path. The separate MurmurHash implementation XORs
character codes into a numeric accumulator and formats a base62 hash. It never
reconstructs JavaScript or passes its result to eval. These behaviors agree
with the package's compiler purpose; no deployment-specific intent is assumed.

Two call-fact matchers incorrectly treated the arguments in
`eval('require')(pluginPath)` and `eval('require')(path.resolve(configPath))`
as arguments to eval. Tree-sitter now requires the actual callee and first
argument. Later eval arguments and calls to the evaluator's result do not
satisfy the variable/call-result rules. Real eval arguments still match even
when the resulting value is subsequently invoked.

The retired `js-near-xor-eval` objective required only character-code XOR and
variable eval within 64 lines. Neither decoding nor data flow was required;
minification made unrelated webpack modules qualify. No YAML consumer selected
that rule or its ancestor directories; the sole explicit reference was a
negative expectation. Its neutral arithmetic and evaluation observations stay
available separately. The existing
`objectives/anti-static/obfuscation/encoding/xor::character-xor-eval` requires
character reconstruction and remains the canonical suspicious detection.

Run the focused controls without executing JavaScript:

```sh
python3 testdata/relay-eval-callee/check.py --scratch /tmp/relay-controls
```

The controls cover actual JavaScript and TypeScript eval arguments, an invoked
eval result, returned require calls, later arguments, quoted calls, unrelated
hash/eval functions, and XOR reconstruction followed by eval. The existing
`obf-xor-eval-spawn-stage.js` hostile fixture retains its fetch/XOR/eval/detached
spawn detection. The obfuscator option-surface control remains free of hostile
or suspicious findings. A separate Forager-recovered
`rand-user-agent@1.0.110` archive retains every prior trait, including its five
suspicious permutation-loader findings. Recovery artifacts and `.forage.json`
provenance are in the task scratch directory; unavailable coa/flatmap-stream
releases were not replaced with reconstructed fixtures.

Relay's archive-level hostile/suspicious counts changed from 0/1 to 0/0;
each minified bundle changed from 0/1 to 0/0 (two leaf occurrences total).
The only lost findings are the invalid decoding objective and the two
incorrect argument-shape observations, including their source-file and CLI
bundle occurrences. Hashing, module loading, process execution, and filesystem
signals remain. Atomscan's ML verdict is benign before and after; its overall
probability changes from 0.7717416 to 0.6486221 (npm specialist: 0.049340695 to
0.007397026). The old model reports feature schema v18 versus engine v21;
this assessment does not use its score as behavioral evidence.
