# Distinct method controls

These inert Go programs expose method names and constant strings. The focused
checker scans copies outside the fixture tree; it never executes the binaries.
Each source program can be rebuilt from `src` with:

```sh
GOOS=darwin GOARCH=amd64 go build -trimpath -o ../distinct-methods.macho ./distinct
GOOS=darwin GOARCH=amd64 go build -trimpath -o ../repeated-method.macho ./repeated
GOOS=darwin GOARCH=amd64 go build -trimpath -o ../repeated-report.macho ./repeated-report
```

The positive exposes three distinct profile methods and all three reporting
methods. The two negatives repeat only one profile or reporting method. Wallet
address extractor names appear in all three. These controls test the static
inference, not real network activity or extraction of secrets.
