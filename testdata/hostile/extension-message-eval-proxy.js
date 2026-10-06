// Minimal message-driven eval proxy: a runtime.onMessage listener that
// evaluates sender-supplied code in a tab's MAIN world via scripting.
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg && msg.type === "probe:eval") {
    const target = msg.tabId || (sender.tab && sender.tab.id);
    chrome.scripting.executeScript({
      target: { tabId: target },
      world: "MAIN",
      func: (src) => {
        try {
          return { ok: true, value: (0, eval)(src) };
        } catch (e) {
          return { ok: false, error: String(e) };
        }
      },
      args: [msg.code || "1"]
    }).then(
      (shots) => sendResponse({ ok: true, result: shots[0] && shots[0].result }),
      (err) => sendResponse({ ok: false, error: String(err) })
    );
    return true;
  }
});
