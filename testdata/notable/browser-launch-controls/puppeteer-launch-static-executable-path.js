// Benign control: browser automation with a statically resolved browser.
// Shares the puppeteer.launch primitive with fetched-binary droppers, but the
// executable path is a local install location, not a runtime-fetched payload.
const puppeteer = require('puppeteer-core')
const fs = require('fs')

const CANDIDATES = [
  '/usr/bin/chromium-browser',
  '/usr/bin/chromium',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
]

function resolveExecutablePath() {
  return CANDIDATES.find(fs.existsSync)
}

async function main() {
  const executablePath = resolveExecutablePath()
  const browser = await puppeteer.launch({
    executablePath,
    headless: 'new',
    args: ['--no-sandbox'],
  })
  const page = await browser.newPage()
  await page.goto('https://example.com', { waitUntil: 'networkidle2' })
  console.log(await page.content())
  await browser.close()
}

main().catch(err => {
  console.error(err)
  process.exit(1)
})
