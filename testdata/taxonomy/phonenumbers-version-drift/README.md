# phonenumbers v1.0.66 review

Verdict: **BENIGN**. This is `github.com/nyaruka/phonenumbers`, a Go port
of libphonenumber for parsing, validating, formatting, geocoding and carrier
and timezone lookup. All runtime library code and build tools are identical
to v1.0.65.

## Release comparison

Both releases were fetched from the Go module proxy:

- https://proxy.golang.org/github.com/nyaruka/phonenumbers/@v/v1.0.65.zip
  SHA256 `29868cb2f91cf7b5cff1f8b74c5a0075f673a3377031abdaa8ce7e9731b34844`
- https://proxy.golang.org/github.com/nyaruka/phonenumbers/@v/v1.0.66.zip
  SHA256 `ec3d673ef56418d7fe102544dd60ae3072286805347661e8257904a4059ce106`,
  identical to the submitted sample.

Only five of the 29 members differ: `metadata_bin.go`,
`prefix_to_carriers_bin.go`, `prefix_to_geocodings_bin.go`, the changelog,
and the test file. The changelog says "Updated metadata"; the test adds
`+2250749195919` as a possible Côte d'Ivoire number.

All 45 Base64/gzip literals in each release were decoded. The region,
timezone, carrier and geocoding tables were parsed using the actual binary
format: little-endian value-table length, newline-separated UTF-8 values,
mapping count, delta-varint integer keys, and interned uint16 values (with
uint8 array counts for regions/timezones). Every table consumes its entire
input. Comparing reconstructed maps rather than compressed bytes removes
Go map iteration and string-intern ordering differences.

- The 215 country-code mappings (246 region values) and 3,234 timezone
  mappings are unchanged. Both source files are byte-identical.
- Of nine carrier-language tables, only English changes: five mappings
  update Moov's Côte d'Ivoire prefix, add SingTel prefixes 658036/658037,
  and add Digicel prefix 6769.
- Of 33 geocoding-language tables, only English and French change, with
  24 mapping changes each for Côte d'Ivoire prefixes.
- The metadata protobuf grows from 179,536 to 179,562 bytes. Calling the
  reviewed exported `MetadataCollection` and comparing its JSON output
  shows changes only to numbering regexes/formats for CI, IR, SG and TO.
  Both collections have 246 records. No executable content was introduced.

`countrycode_to_region_bin.go`, the originally flagged small carrier, has
SHA256 `7aad6f84905b170a3363d58f19be4f21984d51372672b8db5b52406d129ad37a`
in both releases. A current scan also flags v1.0.65's compressed literals;
the original queue's clean baseline does not demonstrate a code change.

## Execution and effects

`init` calls `loadIntStringArrayMap(regionMapData)`, then initializes phone
metadata with `loadMetadataFromFile`. `MetadataCollection` calls
`decodeUnzipString(metadataData)` and `proto.Unmarshal` into the generated
`PhoneMetadataCollection` schema. `decodeUnzipString` performs standard
Base64 decoding, gzip reader construction and a memory read. The lookup
loaders reconstruct integer-to-string maps; the library then uses these
values as numbering regexes, formats, names and locations. Carrier and
geocoding tables are loaded lazily with `sync.Once`. These paths neither
stage executable files nor execute the decoded bytes.

The separate `cmd/buildmetadata` tool fetches Google's libphonenumber data,
exports its carrier/geocoding resources with `svn export` through Bash,
serializes protobuf/maps, compresses them and writes generated Go files.
Its URLs, commands and code are byte-identical in the preceding release.
It is an explicit developer command, not a new import-time downloader.
The shipped site uses jQuery from a CDN, also unchanged. Network, shell,
write and codec findings remain notable.

## YAML corrections and preservation

1. Require a string/quote/whitespace boundary before the Windows device
   namespace. The original text matcher read `\\.\uFF0E` inside a phone
   extension regex character class as a device name. Runtime and escaped
   device paths, including GUID names, still match. Named pipes, mailslots,
   WMI roots and UNC paths remain excluded. Keep the original notable
   criticality; this is a matcher correction.
2. Move `go-write-method-call` from `process/io/stream` to
   `data/buffer/transfer`, preserving its matcher, platform/type scope,
   confidence and notable criticality. Calls such as `bytes.Buffer.Write`
   and the library's builder writes do not establish process I/O. The
   destination already holds generic stream-buffer transfers. Both exact
   objective consumers now use the new ID. Auditing selectors for both
   leaves and all ancestors found no directory-reference consumers.
   Update the earlier package-source fixture expectations and ID map.

Run `python3 testdata/taxonomy/phonenumbers-version-drift/check.py` from
the repository root for the five focused positive/negative/both-claims
controls. The package's `go test .` also passes.

## Analyzer limitation

The sole suspicious trait ID is the engine-emitted
`binary/embedded/base64-gz`. Its synthetic records are made directly in
`embedded_code_detector.rs::detect_base64_binary`, with suspicious severity
and T1027.009 assigned from encoding/container magic alone. They do not
receive ordinary YAML evaluation with the parent's facts; the existing
YAML hook/exception cannot remove them in this analyzer. No YAML shadow or
package-name allowlist was added. The unsupported concealment interpretation
requires an engine correction, as already documented by the Collector esc
asset review. The retained finding does not change this sample's verdict.
