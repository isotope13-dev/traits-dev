PyArmor recovery belongs in `../filefacts/src/formats/pyarmor.rs`, with bounded
marshal normalization in `pyarmor/marshal.rs`. Cleave pairs protected modules
with companion runtimes through `src/analyzers/archive/pyarmor_members.rs`.
The former Cleave-local decoder is removed. Historical prototype files in the
PE triage audit are retained as evidence; their installer is disabled.

The decoder recognizes a protection layout, not a specimen name. It supports
reviewed PyArmor 8/9 container layouts, nondefault numeric runtime serials,
parsed Python bytes literals and embedded binary containers. Runtime key recovery
recognizes masked or unmasked DER key candidates independently of PE/ELF/Mach-O
packaging. A bounded PE section search remains as a compatibility fallback.
Cleave routes ZIP/VSIX, tar-family and PyInstaller members through this API.
A standalone input can be recovered with an explicitly supplied runtime:

```sh
cargo run --manifest-path ../filefacts/Cargo.toml --example pyarmor-recover -- RUNTIME INPUT OUTPUT_DIRECTORY
```

The API normalizes extra PyArmor marshal fields, follows nested code objects,
decrypts descriptor-defined instruction regions, and restores relocated prologues.
Version-selected marshal layouts cover CPython 3.8–3.14; that is not a claim that
every PyArmor build for every Python version has been verified. Output is an
analysis snapshot with counts and explicit limitations, never executable source.
Source literals, native runtimes and specimen code are never executed.

Remaining limits include older/different container layouts, payload-specific
nonce-XOR procedures, mixed-string encryption, native/BCC/JIT code, and
unavailable companion runtimes. Instruction-level nonce-XOR descriptors produce
an explicit partial-recovery diagnostic. Unsupported outer nonce-XOR layouts
fail recovery. Container headers are checked structurally; authentication tags
are not verified. Restored instructions do not reverse transformed identifiers
or reconstruct original source formatting.

Recovery is bounded by input size, object count, nesting, candidate key count,
edit bytes and archive pairing budgets. Missing or unsupported recovery produces
analysis diagnostics rather than a clean or malicious verdict.

Validation on CodeGeeX 2.27.6 (SHA-256
`683a7f3a9faf32a5e35d22b551acf4bf903d408cd768cc905c08f7a194ea40c0`):

- All eight bundled platform runtimes recovered the entry-point container.
- All 61 protected Python modules recovered: 404 code objects and 359 encrypted
  instruction regions; no remaining instruction protection was reported.
- An independent xdis reader parsed all 61 normalized snapshots and all 404 code
  objects. Security-relevant functions were inspected as disassembly.
- Ten filefacts recovery tests cover independent OpenSSL fixtures, nested code,
  relocated prologues, short nonces, serials, platform-independent key recovery,
  malformed/truncated data and explicit partial-recovery status.
- The filefacts unit suite passed: 2,664 passed, 14 ignored. The subsequently
  added prologue test passed in the focused ten-test run.
- Two Cleave pairing tests passed. A complete ZIP scan emitted the expected
  `app.py.0.pyarmor-analysis.pyc` child, with a proper 16-byte PYC header.

The implementations use independently written bounded parsing. Format research
was checked against [Unit 42's technical analysis](https://unit42.paloaltonetworks.com/vvs-stealer/).
The external GPL unpacker was used as a separate static cross-check; its code is
not incorporated into filefacts or Cleave.

Cleave's lockfile now references published filefacts revision
`f84a1e21cc9f250a0bcecb659c2aadf676cb38e6`. Normal Git dependency tests passed
with `--locked --offline` in a checkout of the current Cleave revision. The
verified lockfile replaces two committed conflict-marker sections and lets Cargo
repair their inconsistent dependency entries. The reviewed lockfile diff is
saved as `cleave-dependency-lock.patch`.

The complete VSIX scan finished with 15,215 file records, including all 61
recovered Python children. None of the recovered children or other members had
hostile findings. The two suspicious root findings remain visible: PyArmor
protection and native runtime debugger checks. CodeGeeX is now classified `good`
after reviewing the recovered coding-agent behavior; Hopper recorded the
correction and a dry-run readback returned one noop. Counts are now 61 good,
20 bad, four dual-use and zero inconclusive. Installed filefacts also passed
clippy with warnings denied.
