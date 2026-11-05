# Zig mislabeled-good review, 2026-11-04

`0c57eadaeac7` is a Gentoo build recipe for a Wayland screen locker;
`76e4d4346228` is a Neovim build file; `05c721682718` contains generated
C-to-Zig declarations; and `23f334869f73` is the Bold source package.
`d3198626bbca` and `8e012493b210` are tree-sitter source packages.
Fresh scans found no suspicious or hostile traits. Endpoint rulings: good;
validation passed and Hopper confirmed or moved all six to good.

The Linguist archive `a139df66a1ee` has the same hash as the sample reviewed
in `mirc-good-review-2026-11-04.md`.

`933c11ac647d` is an Nmap source distribution. Nmap's general scanning
function is dual-use, but this archive includes a WebExec exploitation script
that starts operator-supplied commands through a vulnerable service and an
UnrealIRCd-backdoor script that sends operator commands through the backdoor.
Under the endpoint criteria for embedded exploit implementations, the archive
is bad. Two new hostile traits in separate execution and backdoor directories
match the corresponding scripts and propagate to the archive; controls that
remove the service call or alter the backdoor trigger clear the respective
finding. The full archive was rescanned, validation passed, Hopper moved it to
bad, and its relocated copy was hash-verified.

Three Zig compiler packages contain Windows SDK headers that declare Protected
Storage interfaces and WinHTTP Cookie/ETag constants. Those declarations
were previously described as credential theft and command-and-control reads.
They now produce neutral reference observations; a synthetic combination of
the HTTP clues and process creation still produces the stronger hostile
finding, and removing one clue clears it. The compiler packages require fresh
full rescans before a verdict. Their first rescan attempts were stopped because
memory became constrained while other workspace jobs were active.

The other Zig-pool samples remain under review.
