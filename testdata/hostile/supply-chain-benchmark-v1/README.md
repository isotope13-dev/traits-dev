# Supply-chain benchmark v1

This corpus contains 315 package-shaped static-analysis fixtures: 15 per
cleave-supported package-capable source language, split five each across Linux,
macOS, and Windows. Nine scenarios per language conceal their action specification.

Every activated path requires both the random environment-variable name and value
recorded in `manifest.jsonl`. Activation writes only the decoded specification to a
temporary canary file, starts only a harmless local child, and connects only to the
discard port on `127.0.0.1`. Realistic reserved `*.example` hostnames appear solely
in the loopback HTTP Host header. Named credential and persistence targets are never
opened or modified.

Counts: {"c": 15, "csharp": 15, "elixir": 15, "go": 15, "groovy": 15, "java": 15, "javascript": 15, "kotlin": 15, "lua": 15, "objectivec": 15, "perl": 15, "php": 15, "powershell": 15, "python": 15, "ruby": 15, "rust": 15, "scala": 15, "shell": 15, "swift": 15, "typescript": 15, "zig": 15}
