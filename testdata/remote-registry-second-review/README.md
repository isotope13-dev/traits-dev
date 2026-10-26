# RemoteHiveDump second review

Sample: `53da4d2f61f13b2baac1e8a58362bf30aba461aa75e9e1023fdb83b09946d89d`,
`remote-registry-impersonation.cs`, 2,080 bytes. Verdict: **MALICIOUS**.
This identifies a standalone C# credential-access proof of concept, not a
verified malware family or an identified public-registry package/version.

## Source and execution review

The complete source and `cleave facts` were inspected independently of the
scanner's labels. The entry point supplies `args[1]`, `args[0]`, and `args[2]`
as username, domain/server, and password to `LogonUser`, using logon type 3 and
provider 0. Its returned token is passed to `DuplicateTokenEx`, requesting
`MAXIMUM_ALLOWED` (`0x02000000`), SecurityImpersonation (2), and **TokenPrimary
(1)**. The variable name `impToken` does not change the requested token type.
`WindowsIdentity(impToken).Impersonate()` encloses the remote registry work.

`RegistryKey.OpenRemoteBaseKey(LocalMachine, args[0])` supplies the registry
handle used for each subsequent `OpenSubKey`. The targeted keys and operations
are:

* `SAM\Domains\Account\Users`, followed by `GetValue("Names")`;
* `SECURITY\Policy\Secrets`, followed by `GetValue("")`;
* `SYSTEM\CurrentControlSet\Control\Lsa`, followed by `GetValue("Digest")`.

The results are assigned to local variables and discarded. There is no hive
export, per-account/per-secret enumeration, secret decryption, output, staging,
exfiltration, persistence, subprocess launch, or deletion. The use of disposable
contexts and `Undo` is identity restoration, not evidence-removal cleanup.
There are no encoded scripts, concealed payloads, or archive members; C# string
escapes are the only decoding needed for the credential-store paths.

This source does **not** establish a functioning credential dumper. `ctx.Undo()`
is outside the scope of the using-statement variable, so the submitted file
does not compile as written. Native return values are unchecked and native token
handles are not closed. Reading the listed root values does not implement SAM
hash extraction, LSA secret decryption, or the SYSTEM boot-key recovery routine.
No sample code was executed or repaired into an operational dumper.

[Microsoft's LogonUser documentation](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-logonuserw)
also distinguishes local authentication from remote logon and documents the
network-token limitations. [DuplicateTokenEx](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-duplicatetokenex)
duplicates an existing security context; neither that operation nor
MAXIMUM_ALLOWED proves privilege elevation or delegated network credentials.
Successful remote access is consequently not assumed.

The coordinated attempt to access both password/secret stores under an alternate
identity, together with the explicit LSASS-avoidance framing, tips the judgment
toward an offensive credential-access prototype despite those implementation
defects. Authorized assessment or educational use is possible. No such
authorization, package identity, deployment context, or external corroboration
was supplied; the verdict does not allege an observed compromise.

## Rule corrections and preservation

* The old `objectives/credential-access/dump/system::remote-registry-hive-credential-read`
  required a remote-registry operation near any SAM, SECURITY, or Control\Lsa
  path reference. It did not require a read from the referenced key or even a
  credential-bearing key. Before editing, a policy-query variant with only
  SOFTWARE keys and `Control\Lsa\FipsAlgorithmPolicy` reproduced **one hostile
  and one suspicious** finding. The original matcher, scope, proximity, and
  confidence are retained as the notable capability
  `micro-behaviors/os/registry/access::remote-registry-hive-references`, with
  a description of co-occurring references. This preserves its useful evidence
  without claiming credential material was read.
* The hostile impersonation composite moves to
  `objectives/credential-access/registry`. It now requires actual opens of
  both the SAM account store and LSA secret store, remote registry access, and
  an impersonation call expression. A remote policy query or context-type
  declaration alone cannot establish the credential-access combination.
  Its description states the supported combination, not successful extraction.
* Two suspicious atomic rules cover the independently significant SAM-account
  and LSA-secret key opens. Matchers require the relevant `OpenSubKey` call and
  its first path argument, including a path-component boundary. Comments,
  quoted examples, `Accountant`, and `SecretsConfig` are near misses. The
  current call-argument projection treats C# verbatim strings as opaque
  expressions; AST call-node matchers therefore cover both ordinary escaped
  and verbatim strings. Anchoring to the called receiver avoids finding a
  quoted call inside an unrelated invocation's string argument.
* `dotnet-identity-impersonation` previously matched a
  `WindowsImpersonationContext` type name without an invocation. Its matcher
  now requires a call expression, and its description explicitly says
  "reference": comments and quoted expressions remain references, not proof
  of execution. A symbol-only replacement was tested and rejected because the
  current PowerShell facts producer omits the static impersonation call.
  The retained text matcher preserves that PowerShell call coverage.

Before changes, exact-ID and ancestor consumers were inspected. No external
rule referenced either old remote-registry objective ID, and there were no
directory consumers of `credential-access/dump` or `dump/system`. The two
`credential-access` ancestor consumers are JavaScript MCP-configuration rules,
so the new C# credential-store atoms do not broaden them. The registry-access
directory consumer is a registry-write composite; the added capability group
already requires an existing member of the same access directory and cannot
introduce a new matching population there. Existing SAM/LSA path primitives,
token duplication, logon, and remote access detections remain intact.

No pre-existing dedicated remote-registry fixture was found in the available
test corpus or other supplied samples. The submitted positive and renamed,
case-varied, and verbatim variants exercise the retained attack technique.
The existing `testdata/fallout-review/hive-dump.ps1` fixture independently
checks that SAM/SYSTEM/SECURITY extraction coverage outside this batch remains.
Broad reference-only combinations intentionally lose unsupported attack
classification while retaining their notable evidence; the submitted attack
loses no supported behavior coverage.

## Coverage and verification

Controlled local scans use `--no-update --analyze local --mode slow -f json`.
The initial unqualified `atomscan <sample>` and `cleave facts <sample>` were
also run. Before/after reports and facts are in the named scratch directory
`scratch/remote-registry-review` outside the trait checkout.

| Observation | Before | After |
| --- | ---: | ---: |
| Hostile traits | 1 | 1 |
| Suspicious traits | 1 | 2 |
| Notable traits | 10 | 11 |
| Total traits, including low levels | 16 | 18 |
| Classifier probability | 0.99975675 | 0.99979585 |
| Classifier confidence | 100% | 100% |
| Matched FP level | 0 | 0 |
| Archive members | 0 | 0 |

The classifier and manual verdict agree. `flow-query-incomplete` is reported
by the analyzer; source tracing supplies the handle and execution relationships
the current facts graph does not prove. The model bundle also reports feature
schema v18 versus engine expectation v21; no model was changed or retrained.

The one hostile finding expresses one coordinated credential-access technique;
two suspicious findings cover the separate credential stores. Additional
hostile rules would duplicate that technique or invent behavior. Investigation
of token operations, all three registry reads, the using scopes, and the final
Undo found no distinct payload, staging, persistence, exfiltration, elevation,
or cleanup attack to reach the 3–5-hostile goal. In particular, not touching
LSASS is not by itself a security-control bypass, and the LSA configuration
read is not proven boot-key recovery. No confirmed separate hostile behavior
is left uncovered.

Reproduce the fourteen focused positive/near-miss checks outside test-path
suppressors with:

```
python3 testdata/remote-registry-second-review/check.py --scratch <scratch-dir>
```

The checks include the existing hive-dump regression, both single-store
variants, policy-only access, comments, quoted source, quoted calls passed to
another function, context-only declarations, and PowerShell call preservation.
The final repository-wide check is `make validate`.
