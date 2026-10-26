async function installId() {
  const id = crypto.randomUUID();
  await chrome.storage.local.set({ id });
}
async function pulse() {
  await fetch("https://metrics.example.org/activity", {
    method: "POST",
    body: JSON.stringify({ count: 1 })
  });
}
chrome.alarms.create("activity", { periodInMinutes: 240 });
