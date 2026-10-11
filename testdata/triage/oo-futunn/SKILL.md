---
name: connector-example
description: Read connected service data.
---

# Connector example

This guide describes a connector for reading data from an account authorized by the user. Inspect the service contract before building a request, then return the requested records to the user. Authentication is managed by the connected service. The skill does not request local tokens or send records to a separate recipient. The example below documents an optional command for first-time setup. Review the installer before running it; installing software is separate from fetching account records.

```powershell
irm https://downloads.vendor.com/install.ps1 | iex
```
