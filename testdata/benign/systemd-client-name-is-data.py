# Static documentation data, not an HTTP-client command or service installation.
EXAMPLES = (
    "ExecStart=/usr/bin/printf curl",
    "ExecStop=/usr/bin/echo wget",
    "ExecStartPre=/usr/bin/logger curl failed",
    "ExecStart=/usr/bin/curl-wrapper --version",
)
