# BZ2 mislabeled-bad review

Review in progress: 29 artifacts; both scanners completed full scans.

- `b5add0dcc5ce75c19e2af5c9566c449204b77c89247df496e4d5ffa7ed281d56` — **bad** — A ticketing application contains an obfuscated method that reads an embedded resource, transforms it using a repeated CJK marker, Base64-decodes it and loads an assembly for reflective invocation. Static .NET instruction inspection established the sequence. The combined finding matched both scanners on the original compressed artifact; two comparison samples and full validation passed. Hopper confirmed bad; the loaded stage was not executed.
- `8819206811368498419730b1dd0d56018e877d004798747b5f2ef2d6b372641a` — **bad** — Static .NET instruction inspection shows an environment-variable utility reads image pixels and follows a direct call chain to `AppDomain.Load`; it also resolves methods and creates delegates. A combined pixel, assembly-loading, resource-entropy and identity finding matched both scanners; two comparisons and full validation passed. Hopper confirmed bad; the stage was not recovered or executed.
- `f1aaf9b06ba8794832e53b45e560c63b52ba76cb01b2a8d31de8f625d29a1b8d` — **bad** — Static .NET instruction inspection shows the simulator's form initializer reads the blue channel of a bitmap resource, reflectively loads an assembly, enumerates types and creates an instance. A combined pixel, reflection and entropy finding matched both scanners; two comparison applications and full validation passed. Hopper confirmed bad; the stage was not recovered or executed.
- `8799d0d9c137c801525b65cc148fa34997cb6bf7c352fa94736bdf5b7fd1ab80` — **bad** — An order-themed executable combines zero-width identifier obfuscation, reflective resource loading and debugger checks. The new combined finding matched both scanners on the compressed artifact; two comparison controls and full validation passed, and Hopper confirmed bad.
- `8b3227148a76cebba26528fcca582241c63a8523e2655426f6a276ad625fb41f` — **bad** — A football memory game contains reversed names for the Base64 conversion type and method alongside an entropy-rich resource, application-domain loading and reflective invocation. The combined finding matched both scanners on the compressed artifact; two comparison applications were clear, full validation passed and Hopper confirmed bad. The loaded content has not been recovered.
- `1f6e992bb9f1e4ba2640df7f5f44036fd70696c9b3f3d7a18562bb28fbf3b0e2` — **bad** — A game embeds a component combining pixel-channel resource access, Base64 and reversal, decryption, reflection emit, and anti-disassembly. The new combined finding matches the original compressed artifact in both scanners, while two other game samples did not match; full validation passed and Hopper confirmed bad. The decrypted payload was not recovered.
- `22562c62d63015448747d8eff8d0fbe8ca39d0a61ffd9d0fcf3f51c261a0e231` — **bad** — A compressed VBScript uses hidden PowerShell and encoded staging. Both scanners detected it; full validation passed and Hopper confirmed bad.
- `0421436cbfcd3a49518ed1baa10b1ebb8a59296515a89aa861da2bba3bb9fd27` — **bad** — A ZIP contains a citation-themed VBScript with encoded PowerShell and a reconstructed executable. Both scanners detected the chain; validation passed and Hopper confirmed bad.
- `2abc4eca6e91c8766cf9fce20d24ce847fcf17dc3dd67c94d332b12061154258` — **bad** — A RAR inside the compressed stream uses a right-to-left override to make an executable appear to be a PDF. A new path finding matched in both scanners, three negative controls and full validation passed, and Hopper confirmed bad.

The following nine are **bad**: compressed archives contain NSIS executables with payment, quotation or signature document lure names and executable staging. Both scanners identified the combined lure and NSIS payload; validation passed and Hopper confirmed bad.

- `a8077bd92be60da2c6da07d11eb49fbb44c8e46e26a190e59560f3aa9f2b503f`
- `57527f5dbf4716184a8b76cbde61b4ecaf786dba314bb811abb301360a66b899`
- `3474cb43e12ca472dbfbafd53c6c74ce69e31d795a8cdbfac3a5a6fcfb3cedb6`
- `49361497c3e714418cc58f0dbe6fabe434d380d73b48656ef0fac3f1b47a3130`
- `e9ac7b75d3fce7318121fd04c86910feffebde6020e7c7965b045d8c1db7a67a`
- `58641e792b815fd50905667aa6fa2d76a7c71c8ac80ec2e13343075f66e7ae54`
- `4d49c2709ece129193c69e85e9ae32f9e89e501784b205dbbdbc7be10e1361b9`
- `162cf6821dfae176e36afa34e515bb7f815ac8778f79cc2d5446782061813132`
- `c526242199aa951a5a62058eb7566b5d6d0640f9cefcda4a524315801f0d6f38`
