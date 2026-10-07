These fixtures exercise the distinctions changed during stranded-member triage.

- `php-relay.php` transfers read results between a socket and shell pipes.
- `php-unrelated.php` has the same APIs but writes unrelated values.
- `revshell.php` binds the connected socket directly to shell descriptors;
  `php-unrelated-descriptors.php` uses unrelated resources and must not match.
- `lsass-query.ps1` queries a process; it does not dump memory or acquire tokens.
- `uac-name-only.ps1` has an offensive-looking name and an ordinary registry write.

`cases.json` records required and forbidden matches. The PHP relay rule scored
8.0 and the UAC surface rule scored 6.1 in `cleave test-rules`; the positive and
negative fixtures were checked individually; the direct descriptor rule scored
4.0 and rejected the unrelated-resource control. Full extracted-member scans and
reverse-engineering notes are stored outside the traits repository.
