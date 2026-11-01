# Legacy installer staging retirement

The last 13 installer-staging traits moved to package-installation and archive
profiles, installer-hook execution, encoded-shell and interpreter behaviors,
AES key handling, disk-image mounting, and decoded Perl evaluation. The legacy
`objectives/command-and-control/dropper/staging/installer` directory is empty
and removed, and exact consumers now point to the new subjects.

The package/path combinations describe installer references rather than a
proven dropper. Base64 source text, an ad-hoc signed hidden binary, an OpenSSL
password with AES/base64 and a downloaded disk-image mount are not by themselves
hostile; their descriptions and severities reflect the observed evidence. The
IP-address download, executable permissions and background process in an
installer hook, and the encoded Perl execution combination, retain their hostile
classifications. Match conditions, scopes, confidence and proximity constraints
were checked against the original rules.

Xamloader previously required `pkg-payload-reference` in `all` and also had an
`any` alternative for its entire legacy directory. Since that required trait
was a member of the directory, the `any` clause was necessarily satisfied;
its many expanded alternatives were removed without changing that predicate.

The OpenSSL hardcoded-passphrase matcher itself moved from credential access to
crypto key representation. It observes a password embedded in an OpenSSL
command, not a program reading someone else's credentials. Its predicate and
exclusions are unchanged, and all exact consumers were updated.
