# Registry-file mislabeled-good review, 2026-11-04

The pool contains 20 artifacts. The CMake registry fixtures set test values;
the Pygments example contains syntax samples; other registry files configure
fonts, JScript replacement, or Explorer context-menu entries. The IObit
context-menu entry uses hex-encoded UTF-16 command values to invoke the
installed Unlocker and a local script that is not included. The new neutral
hex-text observation exposes the `wscript` prefix; a mutated control does not
match. The pool also contains a Vim distribution ZIP and a Windows utility
installer. The installer retains one suspicious Explorer-policy/API
co-occurrence; its description now states that evidence rather than claiming
that a write occurred.

`5af8b074efd7` is a registry export activating a local IPsec block policy.
Decoded according to Microsoft's [IPsec filter format](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-gpipsec/094f0323-1cae-4b1a-bb46-326bdeb5e77e),
it contains 16 mirrored filters for specific remote IPv4 addresses, applying
to all ports and protocols. Several appear on a [historical malware blocklist](https://gist.github.com/walshie4/6648a23223db413d3b15),
consistent with a protective blocklist; that historical association does not
establish current address ownership. Activating an IPsec policy is not by
itself hostile, so the previous hostile and suspicious claims were relocated
to neutral configuration observations. The fresh scan has no severe traits.

Endpoint rulings for all 20: good. Validation passed and Hopper confirmed all
20 labels. Aside from the installer observation noted above, scans reported
no suspicious or hostile traits.
