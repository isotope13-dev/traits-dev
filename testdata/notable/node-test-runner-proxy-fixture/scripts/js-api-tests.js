// Test runner: stages a fixture node_modules tree for resolver tests.
const fs = require('fs')
const path = require('path')

function stage(testDir) {
  const pkgDir = path.join(testDir, 'node_modules', 'pkg')
  fs.mkdirSync(pkgDir, { recursive: true })
  fs.writeFileSync(path.join(pkgDir, 'package.json'), `{ "main": "./lib/index.js" }`)
  fs.writeFileSync(path.join(pkgDir, 'lib.js'), `module.exports = require('../real')`)
}
module.exports = { stage }
