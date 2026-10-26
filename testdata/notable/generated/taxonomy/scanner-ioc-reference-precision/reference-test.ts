import { it, expect } from "vitest";
import * as fs from "node:fs";
it("checks an IOC", async () => {
  fs.writeFileSync("fixture.js", 'const c2 = "https://scan.aquasecurtiy.org"; const fallback = "https://staging.trycloudflare.com"; const router = "https://npm-cache.com"; const contract = "0xE1f2395ee43e45A1556EC6438a88c31B83493103";');
  const report = await scan({ target: "fixture.js" });
  const finding = report.findings.find(f => f.rule === "IOC_KNOWN_C2_DOMAIN");
  expect(finding).toBeDefined();
});
