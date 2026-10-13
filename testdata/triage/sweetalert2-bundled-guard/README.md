# SweetAlert2 vendored-sabotage guard fixtures

All three tarballs vendor the same region-gated routine (Russian
`navigator.language` plus RU/SU/BY/Cyrillic-RF host check, `swal-initiation`
delay, `pointerEvents` blocking with looping remote audio) inside
`package/dist/bundle.js`. They differ in manifest and disclosure:

- `third-party-bundler.tgz` names `my-app`: the vendored routine is someone
  else's sabotage, so `npm-bundled-sweetalert2-regional-sabotage` stays
  hostile and `sweetalert2-npm-protestware-release` stays absent.
- `genuine-sweetalert2.tgz` names `sweetalert2` with no disclosure notice:
  an undisclosed routine sabotages its users whoever published it, so both
  the bundling claim and the release verdict stay hostile.
- `disclosed-sweetalert2.tgz` names `sweetalert2` and its README documents
  the region-differentiated behavior: both hostile verdicts lift, keeping
  only a suspicious glance at the documented routine
  (`regional-pointer-events-audio-sabotage`).

`check.py` asserts those full-scan criticalities. The publish-root binding
(`metadata/package/name/identity::npm-publish-root-sweetalert2-manifest`)
keeps a nested `node_modules/sweetalert2/package.json` from counting as the
publication's own manifest.
