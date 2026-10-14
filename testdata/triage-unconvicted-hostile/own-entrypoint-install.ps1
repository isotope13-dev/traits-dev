# Fixture: installer references its own documented entry point through
# Join-Path. A bare `\name.js` path is a filename reference, not a dropped
# stage: must match the neutral path atom, never the node stager composite.
$pkgDir = Join-Path $nodeDir 'lib\node_modules\@example\cli'
$entry = Join-Path $pkgDir 'bin\pantheon.js'
$binDir = Join-Path $root 'bin'
if (Test-Path -LiteralPath $entry) { & $nodeExe $entry --version }
