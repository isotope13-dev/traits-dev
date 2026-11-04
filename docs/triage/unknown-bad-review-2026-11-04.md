# Unknown filetype mislabeled-bad review — 2026-11-04

The 39-file snapshot has been classified: 22 bad, 16 good and 1 inconclusive. Detection improvement remains open for one sample whose file type is unknown.

The following 19 tiny DOS programs are bad. Static disassembly shows file search, creation or opening and writes to the found file, or COM-companion creation. The source files are 23–41 bytes and several reuse DOS register state, so these descriptions are static instruction evidence rather than proof of successful execution. Both scanners report hostile findings after the changes:

- `407eb0c52912`, `84a5b5eec947`, `7b45f12e1766`, `26491c3868db`, `46594f039ff9`, `161276d8e2ec`, `dd435c16d245`, `0315e615a57d`, `1ad33a63ea81`, `91eb625b0682`, `d1dd4bcdfb43`, `4c4b55dd26ea` and `a2651950d2e3` search for or open a target and write or truncate it.
- `06cfeac07eee`, `e0d807ef5d2b`, `a10df6aa6d39`, `5a4d46b84a1b`, `65119c11fba4` and `71c5f7c48357` use executable search and companion-style file creation. The indirect form does not independently establish the final name written.

The new and generalized findings cover equivalent register-exchange encodings and tiny inputs. Both scanners match tested originals; controls changing open/write or extension instructions clear the corresponding new findings. Atomscan may still score a control hostile for other reasons.

`701a807d85da` writes one sector to the first fixed disk through BIOS INT 13h and immediately reboots. It is bad. Both scanners detect a copy identified as DOS COM, and changing the write to a read clears that finding. The original is identified as `unknown` and neither scanner applies the file-type-constrained rule to it. This remains an explicit detection gap; no engine feature was added.

`dda1e993f285` is a minimized HTA that starts PowerShell to download and evaluate a remote script. Both scanners match the new combined finding; replacing evaluation with output clears the control. `41a5a0a5ade1` is a large source archive containing executable Office exploit documents in nested test archives; both scanners report the embedded exploit findings. Both are bad.

The following standalone resources are good:

- `048a252135ee`, `a811844c68df`, `4ac4ccd6f070`, `e2016ab93381`, `c2652b280087`, `64a274cb62bd` and `73036dde7c52` are valid GIF country icons. GIF structure inspection succeeded, and both scanners reported no hostile traits or suspicious cleave findings.
- `856260e8f9f6` is a resource-file icon declaration. `e7fc9f336fb7`, `17960dbe5428`, `3d7d3f575d9e`, `1215d92fac8c`, `d9248cf6d4ce`, `fa0c1e4e3fe6`, `1aa874b89372` and `11c6ce119b23` are standalone Cargo manifests whose referenced implementations are absent. Names and dependency features remain available as observations; overlapping suspicious findings based only on those declarations were reduced. The manifests have at most one suspicious finding each and no hostile findings.

`460e19395f87` is a large Node-RED Conda archive. Cleave reported 21,683 extracted entries and Atomscan 19,461, with no hostile traits. The coverage difference and the behavior of the many bundled dependencies could not be independently resolved, so it is inconclusive; Hopper records the ruling through purgatory.
