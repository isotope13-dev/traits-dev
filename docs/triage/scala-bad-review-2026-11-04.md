# Scala filetype mislabeled-bad review — 2026-11-04

The three samples were reviewed: two bad and one inconclusive.

`a926f4cc1faa` connects a socket to an interactive shell and relays both streams. Both scanners already identify the reverse shell; it is bad.

`5b0503945f2d` runs a shell command that downloads an executable to a hidden temporary path, changes its permissions and launches it in the background. It is bad. A new finding combines the Scala shell invocation and the download, chmod and launch facts. Both scanners match; removing the launch clears the control. These are file-level facts and do not prove in every match that the shell invocation and staging commands belong to the same string. The existing suspicious fixture was the same file and was moved to the hostile set.

`dd2df8376c70` is a Mill source archive with 4,250 files and approximately 69 MB of expanded data. Both scanners found no hostile traits, and targeted searches found no host-data-post or explicit exploit patterns; the size and included source, fixtures and assets prevented a complete review. It is inconclusive, recorded using Hopper's purgatory compatibility target.

Full validation passed, and no engine features were added.
