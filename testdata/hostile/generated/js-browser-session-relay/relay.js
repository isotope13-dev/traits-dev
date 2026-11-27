// Synthetic regression fixture: remote job logs in with supplied credentials,
// then returns the browser storage state over the agent's message channel.
const { chromium } = require("playwright");
const { WebSocket } = require("ws");

const ws = new WebSocket("wss://control.example.invalid/agent-channel");

async function runLogin(job) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto(job.url);
  await page.locator('input[type="password"]').first().fill(job.credentials.password);
  const state = await context.storageState({ indexedDB: true });
  ws.send(JSON.stringify({ type: "session_state", storageState: JSON.stringify(state) }));
  await browser.close();
}

ws.on("message", (raw) => {
  const msg = JSON.parse(String(raw));
  if (msg.type === "login_job") runLogin(msg).catch(() => {});
});
