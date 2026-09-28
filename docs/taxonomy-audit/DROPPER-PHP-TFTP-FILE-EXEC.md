# PHP and TFTP file-execution audit

Two legacy download/execute rules have an explicit staged-file launch sink:

- `php-curl-chmod-local-exec` requires a remote curl URL, chmod of a literal
  target, and chmod-then-local-execution within 1,200 bytes.
- `tftp-fetch-shell-execute` requires TFTP command evidence, a local output
  file, and shell execution of that file on one command block.

Both moved to `dropper/file-exec` with matcher bodies and effective scopes
unchanged. The TFTP consumer in `objectives/execution/exploit/memory/offset-cli.yaml`
now references the canonical exact ID. No exact-ID consumers of the PHP rule
were found.

Soft validation passes **1,837/1,837 fixtures**. Strict validation still
reports catalog-wide authoring debt, including **165 over-cap directories**.
