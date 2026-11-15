---
name: local-audit
description: Submit a bundled audit fixture to the approved service.
---

With the operator's approval, submit the included local fixture:

```sh
cd .agent/skills/audit
curl -X POST https://audit.example.invalid/audits --data-binary @a
```
