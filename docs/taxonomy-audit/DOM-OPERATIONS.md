# Generic DOM operations versus browser UI

The XML audit exposed generic DOM operations under `ui/window/dom/{create,tree}`
and `ui/window/dom-access`. Node creation, mutation, selectors, XPath, tree
walkers and text/attribute operations apply to document trees independently of
whether a program displays a browser window. Their canonical home is now
`micro-behaviors/data/collection/dom`, as documented in TAXONOMY.md.

## Changes and boundaries

Twenty-four observations move into the generic DOM leaf, which now contains
25 rules including the previously migrated named-element observation. Every
moved predicate, scope, confidence, criticality, count/proximity constraint and
exclusion is preserved. Qualified consumers follow the new IDs. The ad-blocking
composite's local selector reference is now explicitly qualified too.

Names and descriptions no longer imply browser context from generic operations.
The TreeWalker constructor now says it creates a walker rather than proving
traversal. An appendChild symbol reference says it references that method.
A variable named `node`, `textNode`, `text_node` or `currentNode` does not establish
that it came from a walker; the text-assignment atom and its nearby-walker
composite now describe the actual observations without asserting that data flow.
The composite's matcher remains unchanged, so its consumers retain the same
conditions. Their higher-level claims still require independent relationship
audits; more accurate component labels do not prove those claims.

The sole parent-subtree consumer, Steam extension automation, keeps the original
UI subtree alternative plus the nine moved members formerly beneath that exact
subtree. It does not receive the other DOM observations merely because they now
share the destination leaf. No parent alias or additional umbrella was created.

The [26-entry ledger](dom-mapping.json) records the 24 relocations and the two
special consumer adjustments. Its effective after-definitions verify against
current YAML, and the relocation conditions verify modulo canonical reference
names. Existing qualified references were also updated throughout the taxonomy.

## Verification

The new benign `dom-tree-operations.zip` fixture contains node creation,
insertion/removal, selector lookups, walker construction and text assignment.
It requires the generic DOM hierarchy and forbids the former browser DOM
hierarchies. Before/after scans produce identical finding-ID sets after applying
the migration map, for both archive and member. Fourteen moved observations are
visible in each result. Scores remain 2 for the archive and 1 for its member.

**1,682/1,682 fixtures pass.** Strict validation reports only the existing
**175 oversized directories**; no mixed rule directories exist. The nearby
input-element control continues passing in its current HTML/UI category.
Logs: `/tmp/taxonomy-dom-{before,after}.json`, `/tmp/taxonomy-dom-soft-final.log`
and `/tmp/taxonomy-dom-strict.log`.

## Remaining siblings and precision questions

This batch does not finish the entire UI/DOM audit. DOMParser and HTML parser
references remain under `dom-access` and need a coherent boundary between
markup parsing, parser identity and DOM construction. The existing exclusion
of `text/xml` is not positive evidence of browser interaction. HTML-specific
element creation, page image/anchor selectors, script-URL reads and active-tab
access must be distinguished from generic tree operations and actual rendering.
Do not migrate them wholesale or invent a generic parser bucket solely to empty
an old directory. The broader cap migration also remains open.

Potential validator improvement: flag composites that describe a flow or
relationship but require only nearby APIs and a conveniently named variable.
Distinct matcher bodies and a proximity window do not establish a shared receiver.
