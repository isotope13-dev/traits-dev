// Extension content script: keep the text of every copy in local storage.
document.addEventListener("copy", () => {
  const text = String(window.getSelection() || "");
  if (text) chrome.storage.local.set({ items: [text] });
});
