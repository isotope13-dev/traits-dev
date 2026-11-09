// Benign near-miss: MV3 focus-mode blocker with no campaign IOC. Redirects
// top-level frames to a bundled page, manages tabs without muting audio,
// configures (never opens) the side panel, and blurs a modal backdrop
// element rather than the page root. Must stay below hostile.
async function applyFocusMode(modalOverlayEl) {
  await chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });

  const tabs = await chrome.tabs.query({ currentWindow: true });
  for (const tab of tabs) {
    await chrome.tabs.update(tab.id, { active: false, pinned: false });
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => {
        modalOverlayEl.style.filter = "blur(6px)";
      },
    });
  }

  await chrome.declarativeNetRequest.updateDynamicRules({
    removeRuleIds: [11],
    addRules: [
      {
        id: 11,
        priority: 1,
        action: {
          type: "redirect",
          redirect: { extensionPath: "/pages/focus.html" },
        },
        condition: {
          urlFilter: "*",
          resourceTypes: ["main_frame"],
        },
      },
    ],
  });
}
