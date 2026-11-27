// Synthetic regression fixture: an end-to-end test logs in and saves storage
// state to a file for later tests. Nothing is sent over a message channel.
const { test, expect } = require("@playwright/test");

test("user can log in and reuse the session", async ({ page, context }) => {
  await page.goto("https://app.example.invalid/login");
  await page.fill('input[type="password"]', "test-password");
  await page.click('button[type="submit"]');
  await expect(page.locator("h1")).toBeVisible();
  await context.storageState({ path: "playwright/.auth/user.json" });
});
