// Synthetic regression fixture: automated password login that calls an external
// CAPTCHA solver. No session state leaves the process.
const { chromium } = require("playwright");

async function solveAndLogin(url, username, password) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto(url);
  await page.fill('input[name="user"]', username);
  await page.locator('input[type="password"]').fill(password);
  const body = JSON.stringify({ clientKey: "placeholder", task: { type: "ImageToTextTask" } });
  await fetch("http://2captcha.com/in.php", { method: "POST", body });
  await browser.close();
}

module.exports = { solveAndLogin };
