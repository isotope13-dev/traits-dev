# Telemetry API

Trace requests are sent with the session credentials, and the default exporters are disabled.

| Header | Behavior |
| --- | --- |
| `Access-Control-Allow-Credentials` | Set to `true` for credentialed proxy requests. |

The collector URL is configured with `proxy`. The skill encodes nothing; query values are
percent-encoded in the trace URL, so a return URL is redacted as a whole.
