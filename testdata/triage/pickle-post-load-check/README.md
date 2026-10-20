# pafex 2.3 review

Sample SHA-256: `081ca1d3213e0fdea322b9bb8ef23fdc0dc04f7f36eb20d94e223997c3e4a2c6`.

Verdict: **MALICIOUS**, the configuration-loader dependency in the reported
resion campaign. This wheel supplies the execution primitive; it does not
contain the consumer's executable pickle, downloader, or persistence code.

## Behavior established from the wheel

All eight archive members agree with the extraction, and every populated RECORD
hash and length verifies. There are three unobfuscated Python modules and no
third-party dependencies, embedded payload, startup hook, or referenced URL.
The decoded byte escapes are gzip and XZ magic bytes.

Importing the package defines and re-exports its API. A consumer must call
`load_config`. Without an explicit path, that call passes the caller's frame
globals to a resolver which selects `default.config` beside the caller module
or in its package. The reader validates an eight-byte truncated MD5 and a
four-byte big-endian length, optionally decompresses gzip/XZ/zlib data, and
calls unrestricted `pickle.loads`. Only afterwards does it require a dict and
recursively restrict values to plain types. An attacker can recompute the
unkeyed checksum, and a reducer can execute and return an ordinary dict.

A controlled, harmless reducer appended an in-memory event and returned a dict.
Calling `load_config()` from a synthetic consumer beside that config executed
the reducer successfully for raw, gzip, XZ, and zlib envelopes. Ordinary
save/load round trips also passed for all four formats. No campaign payload was
executed. Writes use a temporary file, replacement, and failure cleanup.

## Provenance and limits

[Kamil Mańkowski's package analysis](https://bad-packages.kam193.eu/pypi/package/pafex/)
specifically identifies pafex as the loader for resion's disguised pickle.
[GHSA-pqqp-5w2f-783q](https://github.com/advisories/GHSA-pqqp-5w2f-783q)
and the originating OpenSSF MAL-2026-18094 record repeat that relationship.
The report describes PTH persistence and next-stage download in the consumer's
pickle, with a stub final payload during analysis. Those are contextual reports,
not findings established inside this wheel. Both pafex and resion's live PyPI
JSON endpoints returned 404, so the consumer was not recovered or independently
reversed in this review. No machine deployment context is available.

The precise match between the independently traced loader mechanism and that
reported distribution role tips the sample verdict. Unsafe serialization alone
would not establish malicious intent. Its standalone trait coverage is therefore
two suspicious observations, with no hostile trait inferred from the report.

## Rule changes and controls

The retired objective
`objectives/supply-chain/hidden-payload/staging/loader::caller-frame-resolved-pickle-config-loader`
required only pickle read/write and nearby frame inspection. It did not bind a
config path to the pickle or establish automatic import-time execution. Its
matcher, scope, proximity, and exclusions are retained as
`micro-behaviors/data/serialize/unsafe::python-pickle-roundtrip-caller-frame`.
The corrected name states co-occurrence, and suspicious severity replaces the
unsupported hostile supply-chain claim. No exact consumer references the old ID.

`python-pickle-post-load-dict-check` independently identifies the ineffective
validation boundary, binding the checked result to an unrestricted unpickle in
one function. The guarded and direct fixtures must match. Checks of another
identifier, checks in another function, and JSON parsing must not match.
Overwriting the result inside the try block or a finally clause must not match.
`python-lzma-compress` adds the missed notable compression call. Existing
compression directory consumers describe compression evidence and remain valid;
the sample already supplied gzip and zlib evidence to those unions.

Seven firing Python metadata field traits moved from `package/ecosystem` to
their name, version, description, runtime, and license homes. Matchers, scopes,
confidence, and severity are unchanged. Existing exact consumers were updated.
The ecosystem directory's only broad consumers are binary-only Steam rules,
whose scope cannot intersect these pkginfo-only atoms; no selector expansion
is needed. The Python Core Metadata version observation stays in ecosystem.
The resulting neutral category-count changes increase five fixture scores by
one or two points; their individual caps track those observed scores, retaining
the same semantic checks and the does-nothing ban on notable/intent findings.

The post-edit atomscan confirms two suspicious traits, zero hostile traits,
the LZMA call, and the relocated metadata on the wheel and relevant members.
