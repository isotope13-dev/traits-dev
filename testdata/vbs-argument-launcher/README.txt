Focused controls for short VBScript launch helpers.

hidden-argument and case-variant: first argument, inline argument launch, hidden/async flags.
visible-argument: argument launch remains; hidden/async flags absent.
synchronous-argument: argument launch remains; async flags absent.
other-argument: hidden/async flags remain; first-argument launch absent.
commented: new launch and flag detectors absent; argument reference remains.
object-only and argument-only: isolated observations, no inline launch or hidden flags.
All controls must have zero suspicious/hostile findings.

environment-fragment.js: Unicode replacement and concatenated env fragment, without execution.
The moved rule belongs in data/string/replace; it must not contribute to an exec directory selector.

The short-source YARA matchers inspect the first 4096 source bytes because cleave
reports zero extracted text runs and skips ordinary atoms for the 78-byte launcher. Offsets are a source
prologue limit, not an exact-size or hash fingerprint. The inline receiver binds
the launch and window flags to WScript.Shell rather than an arbitrary Run method.

Run: python3 testdata/vbs-argument-launcher/check.py
