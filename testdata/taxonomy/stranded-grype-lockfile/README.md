Grype and stranded npm lockfile controls

Build `api-lookups.c` as a host executable and cross-compile `go-symbols.go`
with `GOOS=linux GOARCH=amd64 go build`. Keep generated binaries outside this
repository. Scan the binaries and `positive.py`; copy `lock-v1.json` to the
platform-mandated `package-lock.json` name before scanning it.

Expected observations:
- The C executable calls the actual dlsym API and must retain the lookup trait.
- The Go executable contains a child-command Start method, ordinary Go CPU and
  pool symbols, a struct descriptor, an ELF constant, a MIME type, and references
  to filenames and products.
  It must retain subprocess Start evidence without SQL password-column,
  database-pool, architecture-filename, Node-runtime or Grype CLI identity
  claims from those references. Its embedded module-qualified parquet symbol
  must not be classified as a dataset filename.
- `positive.py` declares a SQL password column and a parquet dataset path.
- The named npm lockfile declares one resolved URL and one SRI checksum.

The reviewed Grype Xdlsym shim is a two-instruction return-zero stub. A mere
substring in that function name must not be mistaken for the dlsym API.
The constructor-only native Go matcher was retired in favor of the already
observed Start method; source constructor and context-constructor atoms keep
their existing scope and references. No blanket product exception was added.

Run `python3 check_results.py <controls.jsonl>` against the four-file scan.

Grype native recovery reached Rizin's 600-second limit. Go's own `nm` and
`objdump` provided complete symbol names and targeted disassembly for the entry,
scanner, database, and credential-helper paths. The final identity matcher is
pinned to `.gopclntab`, so a product-name string elsewhere cannot identify a
binary as Grype. The subprocess observation also accepts the exact Start-method
entry in that native table, preserving this capability when disassembly times
out. The final atomscan run uses a bounded Rizin timeout; this does not replace
the independent Go execution-path review.

The architecture-name heuristics require lowercase suffixes; ELF enum constants
such as ELFOSABI_ARM do not establish an executable filename. Vendor MIME types
such as application/vnd.apache.parquet do not establish a dataset file path.
The Start-method grouping may be filtered from scan output as a low-value OR;
its notable native-table constituent is the assertion used by the control.
