# Harmless static Mach-O controls

These files are analyzed, never executed by the regression script.

- `math-shell.macho`: eight imported math APIs and system("true"). No cipher.
- `math-shell-padded.macho`: the same code plus an uncalled NOP function, making
  the code/C-string ratio exceed 500. This is a neutral layout observation.
- `math-exports.dylib`: local functions exported under math names; no math imports.

Source is included. Build each C file with
`clang -target arm64-apple-macos11 -fno-builtin -O0 -c INPUT -o OUTPUT.o`.
Build padding.s with the same target. Link executables using
`ld64.lld -arch arm64 -platform_version macos 11 11 -undefined dynamic_lookup`,
adding padding.o for the padded control. Link the exports object with `-dylib`
and `-install_name /usr/local/lib/libmath-control.dylib`. sha256.json pins the
checked-in binary artifacts.

Run `python3 scripts/check-macos-math-imports.py --cleave /path/to/cleave`.
The check requires zero hostile/suspicious findings, eight notable imported math
APIs only on the importing controls, neutral shell/math co-occurrence, and a
notable code/string ratio on the padded control. Obsolete objective/ratio aliases
must be absent.
