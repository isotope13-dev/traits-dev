// Benign control: a focus-gate extension parks a distracting tab on one of
// its own pages. The destination is extension-local (runtime.getURL), so no
// remote endpoint ever sees the navigation.
export async function parkTab(tabId, domain) {
  await chrome.tabs.update(tabId, {
    url: chrome.runtime.getURL(`gate.html?domain=${encodeURIComponent(domain)}`),
  });
}
