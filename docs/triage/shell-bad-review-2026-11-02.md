# Shell queue review: archive with obfuscated browser modification

The archive `4c0070ece6f18b13aac8c2448a9f992c64f22c06825b5f1e1e485610afa9c938`
is an altered Python license-expression source package. It is **bad**: its
`src/license_expression/__init__.py` contains an obfuscated Windows payload,
not just the ordinary library code suggested by the archive name.

Static evaluation of the integer expressions used to construct strings shows
that install/build handling installs `pypiwin32`, searches shortcut locations,
modifies browser shortcuts to load an extension, and writes extension code with
clipboard access and replacement of Ethereum-style wallet addresses. The
payload contains a hard-coded replacement address. This assessment did not
execute the package or the payload.

The installed Atomscan reports multiple obfuscation findings but misses the
shortcut modification. The current local rules now detect that behavior by
combining the shortcut creation and save calls, launch-argument assignment,
target-path reference, directory walk, and obfuscation. The decoded strings
were not present in `cleave facts`, so browser-extension and clipboard
behavior still need coverage. The archive has not been relabeled: full
repository validation fails on taxonomy errors, and coverage remains incomplete.

# Modified OpenSSH source archive

Archive `6a9c230c4239775bab6600315586030fe185493106b0a13b83abb8629da9c4e0`
contains modified OpenSSH 5.9 source and is **bad**. The server authentication
code accepts a password assembled from character assignments and appends user
credentials to a concealed log. The client authentication code also appends
the entered password and destination to a log before sending authentication.
The installed scanner detects the server credential capture and bypass but
misses the client capture. A local source rule detects the latter; replacing
the logged password with a redacted value prevents the match. Relabeling is
pending a successful full validation and review of the archive's findings.
