# ELF download-to-shell stdin audit

Two composites directly identify shell source supplied by a download pipe:

- `hex-encoded-iot-shell-stager` requires a hex-encoded wget-to-shell command
  plus NVMS targeting and `/proc/net/tcp` evidence.
- `raw-ip-iot-download-pipe-exec` requires an HTTP IP literal, a native
  wget/curl-to-shell marker, and the Mirai credential table.

Both now live in `dropper/interpreter-stdin`. The shared
`native-download-pipe-shell` atom remains in the source leaf and is referenced
by exact ID. No external exact-ID consumers were found. Matcher bodies,
platforms, and file scopes are unchanged.

Soft validation passes **1,837/1,837 fixtures**. Strict validation still has
catalog-wide cap and authoring debt, including **165 over-cap directories**.
