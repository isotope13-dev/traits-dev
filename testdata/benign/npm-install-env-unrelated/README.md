# Unrelated install, credential-name and HTTP observations

The postinstall entrypoint only prints a build-complete message. The exported
environment diagnostic returns matching names, not their values. The independent
HTTP function sends a fixed status document and never imports the diagnostic.
Nothing in the package sends environment values or credential files.

This controls against archive-wide co-occurrence being labeled as install-hook
credential exfiltration. The hostname is a reserved example domain; it is not
an exclusion used by the detection rules. Analyze the package statically; do not
install or run its contents.

Rebuild the checked-in archive from the repository root without executing code:

```sh
tar -czf testdata/benign/npm-install-env-unrelated.tgz \
  -C testdata/benign/npm-install-env-unrelated \
  package.json scripts/build.js lib/environment.js lib/status.js
```

The README stays outside the archive so verdicts do not depend on this explanation.
