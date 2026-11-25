// Near miss: posts a non-Steam preference cookie as JSON to the vendor API.
async function reportTheme(id) {
  const t = await chrome.cookies.get({ url: "https://app.vendor.example/", name: "theme" });
  return fetch("https://api.vendor.example/prefs", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ id, theme: t?.value || "" }) });
}
