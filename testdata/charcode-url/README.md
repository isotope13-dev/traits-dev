# URL replacement provenance regression

Mermaid 9.1.6 is benign. Compared with the npm 9.1.5 tarball, both development
bundles contain the same four `String.fromCharCode` calls in `removeEscapes`
(Unicode, hexadecimal, and octal text decoding). Their `getUrl` helper escapes
parentheses in the current page URL for SVG marker references. The two helpers
are 3,628 bytes apart, but no decoded value reaches the URL replacement.
The old 4,096-byte composite falsely inferred a relationship from proximity.
This proximity also exists in 9.1.5 under the current rules; the supplied
version-drift alert does not correspond to a newly introduced URL behavior.

Fetched predecessor: https://registry.npmjs.org/mermaid/-/mermaid-9.1.5.tgz
Both source-map inventories retain the same dependencies and source contents
except class tooltip lookup/rendering, flowchart tooltip line breaks, and
mermaidAPI diagram registration/configuration. Ignored `fs` module paths
change with the builder's checkout. The package manifest changes only version.
The emitted JavaScript diffs agree with the source-map changes, plus webpack
import renumbering and the embedded manifest version. No injected payload,
new endpoint, or new execution behavior appears in either development bundle.

The replacement trait now follows argument 1 of a URL-named variable's
`replace` call to `String.fromCharCode`, including local aliases. Its neutral
string-transformation claim belongs in `micro-behaviors/data/string/replace`
at notable criticality: this relationship alone proves neither a hostname
change nor an attacker objective. The unrelated-decoder fixture reproduces
the former false positive; the search-only fixture checks argument position.

Verified each fixture with `cleave --traits-dir . test-rules --rules
micro-behaviors/data/string/replace::js-url-charcode-replacement <fixture>`.
`cases.json` records the expected matches for corpus runners.
