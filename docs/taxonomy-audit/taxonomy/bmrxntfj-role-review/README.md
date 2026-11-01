# bmrxntfj role migration

The bmrxntfj family combines a wallet-stealer indicator cluster with its
NuGet loader profile. Both belong to the same stealer family, so the rules
moved unchanged from `well-known/malware/supply-chain/bmrxntfj-nuget` to
`well-known/malware/stealer/bmrxntfj-nuget`. No YAML references to the old
namespace were found.

The synthetic PE fixtures derive from the existing
`testdata/notable/generated/fallout-current-review/qualified-name.exe`. Both
name the family staging path; only the positive contains the Edge IElevator
GUID. Cleave reported the moved hostile IOC cluster on the positive, and only
the independent staging-path observation on the near miss. The fixtures were
scanned as data and were not executed.
