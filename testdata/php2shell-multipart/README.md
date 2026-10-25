# Empty multipart part sequence

Move `objectives/execution/exploit/file-upload::empty-file-before-next-part`
to `micro-behaviors/communications/http/message::empty-file-before-next-part`.
Its matcher proves only an empty filename followed by another form-data part,
which is a neutral protocol observation. Preserve its exact matcher, name,
description, confidence, notable criticality, file types and platforms. Remove
the inherited T1190 mapping: the sequence alone does not prove exploitation.

The only direct consumer, `empty-first-server-script-upload`, now references
the new ID. No YAML parent selector references the old file-upload directory.
All other rules in the source file retain their IDs, matchers and scope.
Existing exclusions of the objective directory should continue to exclude
objectives, rather than acquiring this neutral observation.

The destination is the existing HTTP message leaf: this matcher relates two
parts within a message body. Individual field syntax belongs in `http/form`;
HTTP upload operations remain in `http/upload`. An empty part
followed by another part is positive evidence; a sole empty part followed only
by the closing boundary is a near miss. Both are exercised in the PHP2Shell
fixture set under Cleave's `tests/fixtures/php2shell-multipart`, together with
ordinary nonempty uploads and separate depth/count boundaries. The new
exhaustion observations remain under `objectives/impact/dos/parser`: they
require deep empty controls or excessive empty controls, not this ordinary
sequence. No MBC mapping is added.
