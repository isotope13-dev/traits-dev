# GIF mislabeled-bad review

The snapshot contains 40 samples. Initial Cleave and Atomscan runs covered all
40, with reference following disabled in Atomscan. Thirty-four structurally
valid GIFs and one inert non-GIF fragment were classified good after both
scanners found no suspicious or hostile traits. Parser validity is not a full
pixel-decode or steganography check. See `gif-good-2026-11-03.md` for hashes.

`d4008e393a2c678f90fabc771ede34b767526a2819913a9c73566298961374e4`
contains a roughly 4.97 MB Base64 run that decodes to a 3,728,896-byte PE
image (SHA-256 `84e0a543df302b18f1188139160fc5a8bd669da071e492453d5d6756064ee568`).
Both scanners report hostile signatures for the extracted PE, including a
UAC-bypass component. The original GIF scan did not recover the PE. A bounded
media Base64 PE recovery path now identifies the embedded image. Both rebuilt
scanners attribute its nested DLL to the recovered PE; Hopper confirmed **bad**.

`4cf49f4aa19ef171a46eb068343e6a67793d12381b60dfef3af11d24aafce910`
contains 26,124 bytes after the GIF trailer. XOR with `0x2f`
recovers a PE image (SHA-256
`0496e0748b7c7a9ebd4c97de5a6e60b93da111cb187a1c09de72e5089ab3d55a`).
Both scanners report firewall-registry and mail-account credential indicators
on the extracted PE. The GIF itself did not surface that embedded file in the
initial scan. A bounded media XOR PE recovery path now identifies the embedded
image, with its firewall-registry and mail-account indicators correctly
attributed; Hopper confirmed **bad**.

`078a133bad32` and `b27f95ed1cc0` contain zero-height remote iframe text after
the GIF trailer. A new suspicious observation describes this text without
asserting browser execution. Both were classified inconclusive: the remote
content and the context in which the bytes would be consumed are unavailable.

`46ac6194e871` has an extension parse failure and a 16,393-byte run of `0x21`.
Two new suspicious observations record the long run and the combination with
the truncated extension; they do not claim the corruption is an exploit. Its
intent cannot be established from the broken file alone, and it is unknown
whether a relevant decoder vulnerability is present, so it was classified
inconclusive. `da19c62ab014` is a 64-byte non-GIF data fragment with no
observed executable content and was classified good.
