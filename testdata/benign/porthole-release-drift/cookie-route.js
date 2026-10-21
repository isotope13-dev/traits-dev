export async function probe(page) {
  const url = "http://127.0.0.1/cookie-policy/";
  await page.route(url, route => route.fulfill({
    status: 200, headers: { "set-cookie": "probe=1; SameSite=None; Secure; Partitioned" },
    body: "<!doctype html><title>probe</title>"
  }));
  await page.goto(url);
  return page.evaluate(() => document.cookie.includes("probe=1"));
}
