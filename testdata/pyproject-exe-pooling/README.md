pyproject/exe pooling must stay root-anchored
===============================================

`pyproject-package-with-exe` pools its legs across archive members, so a
monorepo source snapshot carrying a tooling `pyproject.toml` beside an
unrelated compiler-test Windows binary convicted the whole tree of
"Python-project package contains native binary" (seen on the GraalVM
Truffle Go-module snapshot, which pairs its Python-interop tooling recipes
with a Sulong LLVM-test `hello-windows-link-fembed-bitcode.exe`). The
composite now requires the root-anchored `sdist-root-pyproject-toml` atom,
mirroring the setup.py sibling's `sdist-root-setup-py`.

Run `python3 testdata/pyproject-exe-pooling/check.py <scratch-directory>`.
`flat-dist-positive.zip` (root recipe beside a prebuilt executable) must
report the notable leg and the suspicious parent, with no hostile findings;
`monorepo-snapshot-negative.zip` (nested tooling recipe plus an unrelated
test binary) must report neither.
