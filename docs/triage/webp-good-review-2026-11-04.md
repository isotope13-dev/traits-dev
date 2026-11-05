# WebP mislabeled-good review, 2026-11-04

Nine samples are WebP images (`004b35fa7610`, `8b2521ea0ead`,
`617f6d173f22`, `fc678b6db26e`, `ee5a42402207`, `7b7ef1992e6d`,
`a24fed0ba3ee`, `2d72ab83c6e1`, and `137814f32ef6`). Their RIFF chunk
boundaries match their file lengths; one contains an ICC profile. The local
slow scans report no suspicious or hostile traits. Endpoint ruling: good.

`2e142ed79cc9` is an Arch package, not an image. Its package metadata and
contents describe the Shotcut video editor. The local slow scan reports no
suspicious or hostile traits. Endpoint ruling: good.

Validation passed and Hopper confirmed those ten good labels (no-ops). Two
further archives in this pool remain under review: Cherry Studio source
(`1dd0d5277b26`) and BetterGI (`c0d1109cb9fe`). Initial findings in the latter
include hostile composites built from broad API co-occurrences in bundled
native and managed interop libraries. Three rules asserted a loader,
reverse shell or keylogging solely from co-occurring APIs and constants;
they now report those co-occurrences as capability observations. Fresh scans
of the original OpenCV DLL and the BetterGI executable (including its embedded
interop libraries) match the new observations and no longer report those
three hostile claims. Other suspicious findings and the actual application
behavior remain under review before an endpoint ruling. Validation passed.
Cherry Studio's inline
image data exposed a `/qw4o` malware-family false positive; the rule now
requires that fragment as a URL path, and an actual URL positive control and
the original image negative control have been checked.
