# Security inventory is not process killing

A table containing one or several vendors' AV process names plus process
supervision APIs cannot establish a kill target. Gh0st's AV table feeds its
host report, while termination APIs serve independent command handlers.
The generic API co-occurrence is now notable under
`micro-behaviors/process/terminate/kill::security-name-table-with-termination-apis`.
BYOVD additionally requires known driver and termination-IOCTL evidence.

Run `python3 testdata/security-audit-inventory/check.py <scratch-directory>`.
Both controls contain the same real PE import table for process supervision.
One names several AV vendors; one contains a single vendor and analysis-tool
inventory. Neither may receive any hostile trait. The existing survey,
analysis-tool and TeamViewer-name observations retain their expected levels.
