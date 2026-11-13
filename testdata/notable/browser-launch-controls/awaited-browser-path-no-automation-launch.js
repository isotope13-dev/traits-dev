// Benign control: an awaited browser-path resolver feeding a launcher that is
// not the fetched-binary automation wiring. The executable path is produced
// by a local version lookup against the project's own pinned runtime cache.
const fs = require('fs')
const path = require('path')
const { spawn } = require('child_process')

const RUNTIME_DIR = path.join(__dirname, '.pinned-runtime')

async function resolveBrowserExecutablePath() {
  const marker = path.join(RUNTIME_DIR, 'PinnedBrowserVersion')
  const version = (await fs.promises.readFile(marker, 'utf8')).trim()
  const candidate = path.join(RUNTIME_DIR, `chrome-${version}`, 'chrome')
  if (!fs.existsSync(candidate)) {
    throw new Error('pinned runtime missing; run the sync script first')
  }
  return candidate
}

async function main() {
  const executablePath = await resolveBrowserExecutablePath()
  const child = spawn(executablePath, ['--headless', '--dump-dom', 'https://example.com'], {
    stdio: 'inherit',
  })
  child.on('exit', code => process.exit(code))
}

main().catch(err => {
  console.error(err)
  process.exit(1)
})
