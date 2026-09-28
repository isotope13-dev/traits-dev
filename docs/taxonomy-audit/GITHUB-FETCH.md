# Fetch contents writes require one unambiguous method

`github-contents-fetch-put` restores inline fetch coverage to the GitHub
creation/contents-write combination. It binds the literal GitHub contents URL
and the literal PUT method to the same call. The options object permits literal
property keys and exactly one `method` property, with optional headers/body
fields in either order. Duplicate method properties, spreads and computed keys
cannot satisfy this shape. A GET or a PUT on another call is insufficient.

JavaScript and TypeScript share this observation and its semantic home. It does
not introduce a fetch implementation directory. One atom and one consumer change
are recorded, with 22 exact/ancestor consumer decisions. GitHub now has 84 rules;
167 oversized directories and zero mixed nodes remain.

## Verification

Run the controls without executing their source:

```sh
python3 docs/taxonomy-audit/controls/github-fetch/check.py
```

The controls check both the new atom and its creation/write consumer. Positive
forms include ordinary method/body options, a quoted method key with headers,
method-only options, and a body containing the word `method`. The TypeScript
control uses the same observation. Negative forms include GET, unrelated PUT,
duplicate method override, spread override, computed key and commented code.
Variable-held options are explicitly unsupported, including a later mutation.
The unchanged variable example is a documented coverage gap, not a benignity claim.

Read-only atomscan confirms that the four JavaScript positives recover both
findings, while all eight remaining JavaScript controls lack them. All controls
remain low risk. The full fixture suite passes **1,790/1,790**. Receiver shadowing,
escaped/template URLs, variable-held options and additional HTTP clients remain
coverage/precision work; this matcher is not a whole-program execution proof.

## Engine findings

A trial structured matcher used two predicates on the same fetch call: argument
zero matched the contents URL; argument one's `method` field had a value origin
matching `^PUT$`. That form accepted these counterexamples:

```javascript
fetch(url, {method: "PUT", ...options});
const options = {method: "PUT"};
options.method = "GET";
fetch(url, options);
```

The trial was replaced, not left active. The graph describes value origins;
these results do not prove that PUT remains the selected method. Before relying
on variable-held options, the engine needs an explicit current-field-value
contract covering mutations, aliases and spreads, with these negative controls.
Do not silently reinterpret all existing provenance queries as definite values.

A second discrepancy occurred with a parsed query using zero-or-more property
pairs before/after the method. The standalone Python tree-sitter JavaScript
binding matched the positive, while the checkout engine missed it even in an
isolated trait directory. Nonempty alternatives plus an explicit method-only
case matched correctly in both. The final query uses those alternatives; an
engine/parser regression should isolate the quantified-anchor behavior before
simplifying it. This is an observed discrepancy, not a proven root cause.

The older proximity-based `github-contents-api-write-flow` is still separate debt.
It must not replace destination binding merely to broaden the new combination.
