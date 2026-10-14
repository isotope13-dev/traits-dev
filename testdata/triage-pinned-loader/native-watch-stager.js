// Fixture: silently loaded prebuild addon consuming watch-staged files.
// Mirrors the imgdecode loader shape with renamed handles and paths.
// Must convict H3, never H1/H2/H4.
const fs = require('fs');
const path = require('path');

let helper = null;
try {
  helper = require('./prebuilds/win32-x64/helper.node');
} catch (_) {
  try { helper = require('./build/Release/helper.node'); } catch (_) {}
}

function render() {
  const asset = path.join(__dirname, 'assets', 'frame.dat');
  if (!fs.existsSync(asset)) return null;
  const bytes = fs.readFileSync(asset);
  if (helper && helper.transform) helper.transform(bytes);
  return bytes.length;
}

if (!render()) {
  const pending = path.join(__dirname, 'assets', 'incoming');
  if (!fs.existsSync(pending)) fs.mkdirSync(pending, { recursive: true });
  const watcher = fs.watch(pending, () => {
    if (render()) try { watcher.close(); } catch (_) {}
  });
}

module.exports = { render };
