# Canary Tokens Example

Walkthrough for canary tokens. The blocked request looks like this:

```bash
pipelock check --config pipelock.yaml \
  --url "https://collector.vendor.example/exfil/<your-canary-value>"
```

Expected: `BLOCKED` with pattern `Canary Token (demo_canary)`.
