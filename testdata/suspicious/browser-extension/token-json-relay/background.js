const API = "https://tags.example-saves.test/api/public/ai-tag";

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({ id: "save", title: "Save", contexts: ["page"] });
});

async function aiTag({ url, title }) {
  const { auth } = await chrome.storage.local.get("auth");
  const accessToken = auth && auth.accessToken;
  if (!accessToken) return null;
  const res = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, title, accessToken }),
  });
  return res.ok ? (await res.json()).tag : null;
}
