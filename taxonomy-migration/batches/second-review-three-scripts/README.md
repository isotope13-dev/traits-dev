# Second review of three registry scripts

Judgements derive from the supplied source, not reputation or sample labels.

- `3923eccc3079/import-launch.py`: BENIGN standalone helper wrapper. Python AST
  module statements are imports, an encoded configuration assignment, and a
  function definition. Import does not invoke the helper. Calling `trigger`
  selects an OS/architecture-specific package-side binary, checks existence,
  sets owner permissions if necessary, copies the environment, and launches
  a detached child with suppressed stdio and the configuration as argv.
  Decoded JSON contains home inventory roots, service endpoints and an expiry,
  but no credential acquisition, upload or command dispatch implementation.
  The referenced executable is absent and its behavior cannot be inferred.
- `a5ecc9b9add1/public-secret-dump.js`: MALICIOUS credential publication script.
  A module-level call reads `.npmrc` and `.ssh/id_rsa`, authenticates with
  GITHUB_TOKEN, creates a public repository, triple-encodes the collected JSON,
  and writes it through the GitHub contents API. GitHub decodes the outer API
  transport layer, leaving two reversible Base64 layers around the secrets.
- `c62ce71f4379/public-secret-dump.py`: MALICIOUS Python equivalent, with
  `Path.home`, `read_text`, requests POST/PUT and nested Base64 encoding.
  There is no approval prompt, redaction, destination secrecy, or local-only
  report in either dumper. Credentials become publicly retrievable.

Full source and `cleave facts` were inspected, including decoded configuration,
call arguments and credential-file HTTP body-flow events. SHA-256 values match
those provided. Binwalk is unavailable in this environment; the files are
plain source and contain no executable binary for native disassembly.

## Matcher and placement corrections

- Removed Python evasion composites that inferred concealment from normal
  detached helper setup. Existing process, stdio, chmod, environment-copy and
  encoding observations preserve the supported capabilities without duplicating
  their conjunctions. Relocated the corresponding neutral JavaScript launch
  combination to process creation.
- Moved the parent/dot-directory join from file locations to path operations;
  renamed it to avoid asserting a binary or a resolved path. Updated all exact
  consumers and audited ancestor selectors with repository reference searches.
- Removed the redundant secret-path aggregate and relocated credential-upload
  evidence to capabilities,
  including Vault-read/upload co-occurrence. Existing GitHub theft composites
  retain their source and upload roles.
- Removed a duplicate objective-tier npmrc path predicate in favor of the
  canonical path trait. Moved npmrc/fetch co-occurrence and home/read/path
  observations to capabilities. Removed open-only evidence from the read role.
  The registry-client theft composite now requires credential-to-HTTP body flow
  and lives under credential exfiltration, with consumers updated.
- SSH keyword evidence no longer fires on source object keys. SSH configuration
  matching requires a parser-extracted `.ssh/config` path rather than a private
  key or authorized_keys. Base64/HTTP co-occurrence now requires credential body
  flow, and the multi-store upload description states path-reference breadth
  rather than claiming every referenced store was read.

## Controls and acceptance

The renamed helper fixture is reclassified as benign, requiring its notable
process/configuration observations and forbidding hostile/suspicious findings.
Public-GitHub inventory controls preserve both upload implementations and encoding
while replacing credential stores with package.json/README.md; they must not
trigger credential-publication findings. These distinguish the source role from
ordinary public publishing. Existing references and fixture expectations were
updated together. Hostile composite precision is checked with `cleave test-rules`. The redundant
secret-path union also matched an authenticated SSH example with no file paths;
its removal preserves the body-flow source role without a false observation.

Judgement markers are beside the supplied samples, outside the traits checkout.
