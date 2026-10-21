# Heartbreaker regression evidence

Current placement and verdict follow-up (2026-10-21): see
[minimod-heartbreaker-review-2026-10-21](../minimod-heartbreaker-review-2026-10-21/README.md).
Encrypted replacement/rename is now a neutral notable capability; hostile
source mutation requires the independent ransom-demand composite. The nine
controls below continue to pass. The earlier record follows.

Source: https://objective-see.org/blog/blog_0x8A.html (18 October 2026).
The saved article was only an abstract. The full HTML, its eight article
images, and its code blocks were extracted into the task's scratch directory.
The linked Objective-See HeartBreaker.zip supplied the original Mach-O and
an archived metacore source tree. The public metacore master source was also
read; the article does not establish that metacore is a formal mimicore rename.

The concrete artifact is the embedded Rust source: AES-256-GCM encryption,
truncating writes of nonce and ciphertext, file renaming, and include_str!
source embedding followed by mimicore::morph. The binary's SHA-256 matches
the article's VirusTotal link. No specimen was executed.

## Coverage and limits

The new impact finding requires AES-GCM evidence, an encryption/write
sequence, and file renaming. Source and embedded-source matchers are separate
because binary string extraction splits source lines. Rust source also requires
an actual encrypt call, so commented examples do not supply the operation.
Python follows an encrypt-result origin into write_bytes, then requires a
rename call. These findings describe static relationships and sequences;
they do not prove successful runtime encryption or that every operation uses
the same file handle.

The source-mutation finding requires embedded Rust source plus a real
mimicore/metacore morph call in source, or its code representation in a binary.
It does not depend on the metamorphic marker comments, sample name, ransom
wording, encryption key, suffix, or LaunchAgent label. It describes mutation
machinery, not proof of successful compilation: mimicore is unavailable, and
the article's rebuilding attempt can fail.

Both objectives are suspicious. Encrypted replacement and source mutation
have legitimate uses; these observations alone do not warrant hostile rules.
Raw embedded-source coverage includes Mach-O, ELF and PE. Source coverage
includes Rust and Python with Unix and Windows scopes; no CPU is required.

`sample-results.json` records the final Atomscan results: the original binary,
recovered source, and a renamed/rekeyed metacore variant each fire the two new
suspicious objectives. Full reports, cleave facts, extracted binary strings,
SHA256, PURLS and ENDPOINTS are under scratch/threat-feed/3838. PURLS preserves
unversioned framework names; the absence of their version/revision and of
hostile network endpoints is explained in indicators-notes.md there.

## Corrections to existing detections

The original binary also fired prose-only ransom findings. The following
were retired, rather than using the article's wording as behavior evidence:

- objectives/impact/ransom/note::ransom-deface-phrase
- objectives/impact/ransom/native::your-files-ref
- objectives/impact/ransom/native::encryption-technology-msg

Optional references were removed from the Ruby and Windows PE composites.
Four hostile consumers with a required prose leg were retired instead of
weakening their conjunction: pyc-aead-file-encryption-ransom-demand,
pyc-fullscreen-topmost-ransom-lockscreen,
hash-resolved-chacha-locker-with-ransom-claim, and
ransom-claim-rendered-wallpaper-locker. This intentionally removes coverage
based on those unsupported prose observations.

The generic read_to_end matcher was moved unchanged from
micro-behaviors/communications/http/download/handler::rust-reader-read-to-end
to micro-behaviors/data/buffer/transfer::rust-reader-read-to-end. Its one
explicit consumer was updated. A file read is not an HTTP download; the
remaining HTTP composite still independently requires response-reader context.

## Focused verification

The checker creates controls in the Cleave fixtures tree and statically
analyzes them. It never executes the generated programs. Nine cases cover a
Python translation of the overwrite/rename technique, encrypted copies,
decryption, commented calls, source embedding without mutation, generic buffer
reads, and ransom wording without code. All pass.

```sh
python3 testdata/taxonomy/heartbreaker/check.py \
  --fixtures /usr/local/var/cyclotron/cleave/tests/fixtures/threat-feed-3838-heartbreaker \
  --report /usr/local/var/cyclotron/tmp.noindex/cyclotron-15e998e8/scratch/threat-feed/3838/controls.jsonl
```

The installed Cleave is 3.0.0-beta.2; the sibling source revision observed
during review was 97e53d26fe6630282f76e5cd6b88dc63c0bde30e. Final validation is
`make validate` from the trait worktree.
