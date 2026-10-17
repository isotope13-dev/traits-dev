# postinstall nested subdir install

`install-hook-injects-consumer-dependency` (hostile) convicts a hook
that leaves the package directory and installs something into the
consumer project. The MeanJS-era idiom `cd ./subdir && npm install &&
cd ../..` tripped both legs textually -- the return ascent matches the
escape pattern -- yet never leaves the package: the ascent only undoes
the descent, and a bare `npm install` installs the nested manifest's
own declared dependencies.

`metadata/package/scripts/lifecycle::postinstall-nested-subdir-bare-install`
marks that idiom (descent into an owned subdir plus a bare install with
no package argument and no command substitution). It suppresses the
escape and package-install suspicious traits, which transitively clears
the hostile composite. A nested hook naming a package (`npm install
evil`) matches neither the letter nor the intent of the exception, so
it keeps the full finding.

## Controls

`verify.py` writes synthetic `package.json` fixtures and scans them
with `cleave --traits-dir`:

- `positive/package.json`: `cd ../../.. && npm install evil`. Must
  report the hostile.
- `negative/package.json`: the meanio shape with a bare install. Must
  report neither the hostile nor the escape/install traits.
- `named-nested/package.json`: the nested shape with a named package.
  Must still report the hostile.
