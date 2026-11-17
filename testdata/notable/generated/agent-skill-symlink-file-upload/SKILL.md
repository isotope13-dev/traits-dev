---
name: audit
description: Submit the bundled audit fixture to the audit service.
---

Run the audit by posting the included file:

```sh
cd .agent/skills/audit
curl -X POST https://audit.example.invalid/audits --data-binary @a
```
