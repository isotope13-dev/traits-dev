# Staging carrier review

The `staging/packing` and `staging/steganography` leaves were retired after
reviewing their six composites. Match predicates and scopes are unchanged;
exact consumers were updated to the new IDs.

- The PNG-tail, AES, AppData executable-path and write combination moved to
  `objectives/execution/staging/reconstruct`. The separate combination with a
  detached spawn moved to `objectives/execution/payload/file-exec/detached`.
  The staging rule's cleanup consumer follows its renamed ID.
- MPRESS plus overlay, writable entry and `htons` or socket-send references
  moved to `objectives/anti-static/pack/mpress`. These combinations remain
  suspicious, but neither establishes the function of overlay contents; their
  descriptions and ATT&CK labels no longer assert a network payload.
- OCRA packing with endpoint evidence moved to `metadata/file/profile/network`
  as a notable observation. OCRA with an image-named PE and an IPv4 endpoint
  moved to `objectives/evasion/masquerade/file/double-ext` as suspicious.
  Neither combination alone establishes command and control.
