Docker CLI version drift: BENIGN

Sample: cli@v0.0.0-20190303104010-8ddde26af67f
SHA256: b4bdcabd127df9beb65e59d20b82b8d7adf0a8395ad8e1117cfe2c91bd043edc
Flagged member: cli/compose/schema/bindata.go (Go source, not native code).

Fetched upstream commit 8ddde26af67f9a76734a1676c635e48da4fe8584,
its first parent ee94f72e2c78ef8541550fd585cba33486ccdabb, and earlier
release v18.09.2 (af2647d55b1dff69f5684f5991b9690fddd75c69) through Git.
All 1,242 supplied archive members match upstream Git objects byte for byte.

The immediate merge exports existing connection-helper functions, moving
command-stream connection code into commandconn and exporting SSH parsing.
The flagged bindata.go is identical to the first parent. Relative to the
older release, schemas 3.3 through 3.7 gain additionalProperties:false for
credential_spec; schema 3.8 is added (including max_replicas_per_node).
The generated Base64/gzip byte strings change to represent these schemas.
The generator and decoding/filesystem implementation remain unchanged.

Decoded all nine compressed literals. Each expands to valid draft-04 JSON
and matches its corresponding checked-in config_schema_v3.x.json exactly.
The named observations (2,092 and 2,114 gzip bytes) represent schemas 3.7
and 3.8. No executable content is present in these resources.

Behavior: _escStaticFS.prepare selects an asset, then sync.Once decodes
Base64, constructs a gzip reader and reads into f.data. File() provides a
bytes.Reader implementing http.File. This interface is not a network call.
Validate in schema.go calls _escFSByte(false, schema-name), constructs a
JSON string loader and validates Compose configuration. There is no code
execution, permission change, persistence or exfiltration in this path.
The optional local-filesystem branch opens the named source data file.

YAML correction: moved the sole esc header matcher from
well-known/tool/development/cli/esc::generated-static-assets to
metadata/build/generated::esc-generated-header. A generator declaration
is build provenance, not evidence that the artifact is the esc tool.
Matcher, Go scope, platforms, confidence and notable criticality preserved.
Description now states exactly the observed declaration. No exact ID
consumers existed. Broad identity suppressors lose this false identity;
metadata build suppressors already see go-generated-source-header on the
same marker. No new allowlist or whole-file trust exception was introduced.
Positive, neighboring generator, and header-plus-execution controls pass;
child-process findings remain visible on the execution control.

Final atomscan JSON: zero hostile findings, one distinct suspicious ID
(binary/embedded/base64-gz), repeated eleven times across archive, source
and nine decoded layers. Earlier v18.09.2 bindata.go ALSO fires this same
engine finding today. Thus the stated detection drift does not establish
that compressed resources were newly introduced by this release.

Remaining limitation: the installed engine constructs this suspicious
finding directly in embedded_code_detector.rs, with T1027.009 even for
ordinary resource compression. YAML cannot change its severity or mapping
in this build. The existing fake-basename YAML hook is not a working fix.
Do not claim zero false positives: the residual engine finding is a false
suspicion on benign data and requires an engine change. No engine files
were edited outside the requested traits worktree. binwalk was not on PATH;
source and complete resource decoding were used for behavior analysis.

Marker summary (70 characters, retain verbatim in any commit body):
Docker CLI: ordinary Compose schemas; correct esc provenance placement
