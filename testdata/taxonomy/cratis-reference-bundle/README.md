# Cratis renderer reference assemblies

`Cratis.Stage.Rendering.Cratis` 4.155.0 is **BENIGN**. It renders a compiled
Screenplay model into a Cratis application. Its package declares ordinary
Contracts, Screenplay and Roslyn dependencies; it has no package install hook.

The specimen SHA-256 is
`31788c9994d4a7ec2b9ed97d2bf966da3a840eb611b7a2ebbd851196b3ca9956`.
The immediately preceding NuGet release, 4.154.1, was fetched from
`https://api.nuget.org/v3-flatcontainer/cratis.stage.rendering.cratis/4.154.1/cratis.stage.rendering.cratis.4.154.1.nupkg`;
its SHA-256 is
`89fc9b8c174a3d0a1fb765a374ad9442f39ef1683be3b1622783f1a21970f806`.

ILSpy project decompilation produced 450 files per version: 254 C# files,
168 embedded DLL resources, and other resources/project files. The **only**
difference in those trees is `Properties/AssemblyInfo.cs`: file, assembly and
informational versions, and the recorded repository commit. The commits are
`12aec7a91d4fda946e6108faa77974a8a75b3233` and
`a8dc453d597c6b52579d6238ad3c6814857e2b24`. The outer archives also differ in
NuGet signatures, manifest/package version metadata, DLL and PDB bytes. README
and content-type declarations are unchanged. Thus the reported version alert
is not evidence of newly introduced executable behavior.

Execution-path review explains the matching tokens:

- `StateChangeSliceRenderer` calls `InlineCommandHandlerAdmission.EnsureAccepted`.
  Its lazy reference initializer loads the fixed name `System.Runtime`, then
  uses `MetadataReference.CreateFromFile(assembly.Location)` for Roslyn binding
  analysis. `Analyze` checks the authored handler's syntax and semantic bindings.
- `PureTransitionAdmission.LoadEmbeddedReferences` enumerates
  `PureTransitionReferences.10.0.12.*.dll`, opens each managed resource and
  returns `MetadataReference.CreateFromStream`. These images are compiler
  references, not decoded payloads passed to `Assembly.Load`.
- `SemanticGenerationBodyAdmission.LoadFundamentals` copies the embedded
  Fundamentals reference into `MetadataReference.CreateFromImage`. Its caller
  constructs a Roslyn compilation and checks diagnostics without executing it.
- The embedded cryptography reference has API stubs (`throw null`), not an
  implementation that encrypts user files. The renderer's `Invoke` calls are
  callbacks/delegates for rendering, not an assembly-load-to-MethodBase chain.
- `FrameworkNames.catalog` contains type/member inventories used for naming and
  imports. At DLL offset `0x28f3cd`, `ContainsKey ContentLength` accidentally
  matched the old unbounded `Key Content` pattern. No netsh key retrieval or
  Wi-Fi output parsing exists on this path.

`cleave facts` was inspected including decoded-string records. The framework
schema URIs, generated source/templates and reference metadata explain the
relevant content; random decoder candidates do not establish hidden code.

## Trait corrections

Match conditions and effective file/platform scopes are preserved for the nine
relocated observations. Generic co-occurrence is described as references, not
execution or concealment. Four compound reference observations are now notable
in `micro-behaviors/metaprogramming/reflection`; unsupported T1620/E1059 mappings
and vendor/Reflection.Emit downgrades are removed. The complete AppDomain
accessor observation becomes notable. Partial Load-name variants remain a
component. Encoded text moves to `metadata/file/encoding`, with no claim that it
is decoded or invoked at runtime.

| Old local ID in `objectives/anti-static/obfuscation/reflection/invoke` | Canonical destination |
| --- | --- |
| `dotnet-assembly-load-invoke` | `micro-behaviors/metaprogramming/reflection::dotnet-load-invoke-api-references` |
| `dotnet-appdomain-callbyname-load` | `micro-behaviors/metaprogramming/reflection::dotnet-appdomain-callbyname-references` |
| `dotnet-appdomain-lateget-load` | `micro-behaviors/metaprogramming/reflection::dotnet-appdomain-lateget-references` |
| `dotnet-appdomain-activator-load` | `micro-behaviors/metaprogramming/reflection::dotnet-appdomain-activator-references` |
| `dotnet-appdomain-access` | `micro-behaviors/process/interpreter/runtime/clr::appdomain-accessor-references` |
| `dotnet-assembly-load-token` | `micro-behaviors/os/module/load::dotnet-load-member-name-variants` |
| `dotnet-reversed-assembly-load-token` | `metadata/file/encoding::reversed-load-member-text` |
| `dotnet-base64-assembly-load-token` | `metadata/file/encoding::base64-load-member-text` |
| `dotnet-base64-create-instance-token` | `metadata/file/encoding::base64-create-instance-member-text` |

Exact consumers retain their conditions through the new IDs. The VM instruction
rule's ancestor-directory downgrade retains the moved union through four
references: load/invoke references, AppDomain accessor references, Load-name
variants, and encoded CreateInstance. The other five moved observations imply
one of these, so adding all nine would be redundant. The other broad source
selectors target JavaScript and cannot select these PE/C# observations. No
ancestor selectors target the destination leaves. No directory-wide replacement
broadens existing consumers.

The Wi-Fi rule separately gains English word boundaries and a description
limited to an output-label reference; the Arabic label remains supported.
This is a matcher correction, not a severity-based suppression.

## Verification

Run `python3 testdata/taxonomy/cratis-reference-bundle/check.py` for twelve static
controls (eight inert PE images and four source fixtures). Pass `--sample PATH` repeatedly to check the two NuGet versions.
The controls cover reference-only files, missing invocation/domain/binding
legs, encoded names, English/Arabic Wi-Fi labels and the API-catalog near miss.
A netsh plaintext-key request plus output label must still trigger the existing
native Wi-Fi password-harvest composite. The three C# token-only fixtures exercise encoded text, not valid programs. Test bytes are never executed.

The package rescan must retain the neutral reference observations and emit no
suspicious/hostile traits or false Wi-Fi-key label finding. Finish with
`make validate` after the sample marker is written.
