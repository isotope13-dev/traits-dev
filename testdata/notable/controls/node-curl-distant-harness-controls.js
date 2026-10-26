// Test-harness control mirroring the overturned shape: installer command
// fixtures (curl strings) far from the harness chmod/spawn calls, so the
// download workflow must stay silent.
const { spawnSync } = require('node:child_process');
const EXPECTED = [
  'curl -fsSL --retry 2 -o "$tmp_dir/pkg"',
  'curl -fsSL --retry 2 -o "$tmp_dir/SHASUMS256.txt"',
];
function separator() {
  return EXPECTED.join(String.fromCharCode(10));
}
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
// filler: pushes harness calls beyond the 100-line workflow window
function runHarness(dir) {
  require('node:fs').chmodSync(dir + '/fake-bin', 0o755);
  return spawnSync('fake-bin', [], { cwd: dir });
}
module.exports = { separator, runHarness };
