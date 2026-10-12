# SweetAlert2 vendored-sabotage guard fixtures

Both tarballs vendor the same region-gated routine (Russian `navigator.language`
plus RU/SU/BY/Cyrillic-RF host check, `swal-initiation` delay, `pointerEvents`
blocking with looping remote audio) inside `package/dist/bundle.js`. They
differ only in the publish-root manifest:

- `third-party-bundler.tgz` names `my-app`: the vendored routine is someone
  else's sabotage, so `npm-bundled-sweetalert2-regional-sabotage` stays
  hostile and `sweetalert2-npm-protestware-release` stays absent.
- `genuine-sweetalert2.tgz` names `sweetalert2`: the publication is the
  library itself, so the bundling claim is de-emphasized to suspicious while
  the release verdict still convicts it as hostile.

`check.py` asserts those full-scan criticalities. The publish-root binding
(`metadata/package/name/identity::npm-publish-root-sweetalert2-manifest`)
keeps a nested `node_modules/sweetalert2/package.json` from counting as the
publication's own manifest.
