# Browser recorder and structural controls

`recorder-settings-upload.zip` contains unchanged manifest, settings, content,
background, and offscreen members from the original Plato SDK 2.186.0 wheel
(`eef62895a4ce3af4076b1cad7c40c1aa290b3caa36ebd290f273d844820a4f60`).
These bytes also occur in 2.185.0. Password selectors, IPC, and uploads are
real, but the settings selector is not credential harvesting.

The JavaScript controls test actual same-receiver keyboard fields and a returned
password value. Constant records and different-receiver negatives are stored in
`testdata/baseline/controls/version-drift-recorder/`.

`password-capture-without-controller.zip` preserves the recovered malicious
extension's content script but replaces its background controller with a
logging listener. Retained bytes support password acquisition and messaging,
not remote-control or network-export claims. The capture primitive must match;
the hostile remote-control/capture composite must not.

See [analysis](../../../../docs/plato-sdk-version-drift.md) for provenance,
execution paths, and before/after results.
