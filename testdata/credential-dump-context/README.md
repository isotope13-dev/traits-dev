These benign controls exercise the credential-store dump composite:

- ordinary-helper.ps1: the matching helper name plus filesystem access.
- enumeration-only.ps1: P/Invoke enumeration declaration without password output.
- password-format-only.ps1: example output without native credential enumeration.

Each must have zero hostile findings and at most one suspicious finding.
The real dumpCredStore.ps1 is the positive control: enumeration, password
formatting and helper definition remain required. Its composite precision is 5.8.
