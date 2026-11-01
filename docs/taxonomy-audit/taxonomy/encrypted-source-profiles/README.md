# Encrypted staging: source profiles

Five legacy encrypted-staging rules describe observations in the same source,
not an identified encrypted payload or an activation chain:

- The Go and Python custom-alphabet rules combine Base64 alphabet evidence,
  symmetric cryptography and process creation. Their destination is
  `metadata/file/profile/cryptography`; they are notable profiles rather than
  hostile payload-execution findings.
- The Python and .NET RC4/Rundll32 rules combine RC4, Rundll32 and anti-analysis
  evidence. Their destination is the same profile directory, and they remain
  suspicious: the evidence does not establish what Rundll32 executes or that a
  VM check gates execution.

The predicates, platform and file-type scopes, and confidence values are
unchanged. The descriptions and IDs name the observed combinations; unsupported
ATT&CK and MBC annotations were removed. No other YAML or Markdown file
referenced the old IDs. The destination holds 65 rules after this migration.
