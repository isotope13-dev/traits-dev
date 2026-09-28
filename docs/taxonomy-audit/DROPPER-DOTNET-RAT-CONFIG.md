# .NET RAT configuration leaves encrypted staging

The former `objectives/command-and-control/dropper/staging/encrypted/
dotnet-rat-config.yaml` contained three distinct observations: MD5 and
ECB/zero-padding API markers, a RAT-specific host/port/mutex/install field
cluster, and a composite joining them. These rules characterized a probable
RAT configuration, not payload staging. The composite also did not prove that
the configuration was actually decrypted.

Disposition:

| Former rule | New home | Change |
|---|---|---|
| `dotnet-md5-crypto-service` | `micro-behaviors/crypto/hash/digest::dotnet-md5-cryptoprovider-reference` | API reference, no objective tag; matcher, Windows and `[pe,dll,csharp]` scope, criticality and confidence preserved |
| `dotnet-ecb-mode-config` | `micro-behaviors/crypto/symmetric/config::dotnet-ecb-or-zero-padding-reference` | Capability-level mode reference; matcher, scope, tags, criticality and confidence preserved |
| `rat-config-field-set` | `objectives/command-and-control/backdoor/rat/config::dotnet-rat-config-field-cluster` | Renamed to reflect the bounded field cluster |
| `angle-pipe-config-separator` | `objectives/command-and-control/backdoor/rat/config::dotnet-rat-config-pipe-separator` | Renamed to identify its RAT-config context |
| `dotnet-md5-aes-ecb-rat-config` | `objectives/command-and-control/backdoor/rat/config::dotnet-rat-config-crypto-cooccurrence` | Moved to the RAT configuration objective; “decryptor” claim removed |

The hollowing consumer now references the canonical MD5 capability. The
encrypted-staging `dotnet-ecb-static-key` composite now references the canonical
mode capability. Matcher bodies are unchanged. The MD5 capability no longer
inherits `T1027`, because an MD5 provider reference alone does not establish
obfuscation. The RAT composite retains its former hostile criticality and
confidence: its RAT field cluster and co-occurring crypto markers support that
objective-level inference, while its name does not claim runtime decryption.

Soft validation passes **1,837/1,837 fixtures**. After rebuilding cleave
against the local `filefacts` tree, `make validate` reports the established
**60 strict issues** and **165 over-cap directories**, with no new issue from
this move. The encrypted-staging leaf loses five rules and remains substantially
over the 85-rule cap.
