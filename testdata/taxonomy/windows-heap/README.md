# Windows heap lifecycle fixtures

Six inert PE specimens distinguish HeapFree/LocalFree, HeapReAlloc/LocalReAlloc,
GetProcessHeap and HeapAlloc imports. Each asserts its own observation and rejects
the other five. The case file also reuses eight reference-set consumer controls
to compare complete findings and component edges after the ID moves.

No binary is executed. C signatures are linker scaffolding, not usable API calls.
Build commands and specimen hashes are in `fixture-build.json`. Matchers establish
API references; no runtime call or successful allocation is inferred.
