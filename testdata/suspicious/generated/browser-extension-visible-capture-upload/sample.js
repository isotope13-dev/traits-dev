// Describe the visible tab with a remote API when the shortcut fires.
chrome.commands.onCommand.addListener(async () => {
  const image = await chrome.tabs.captureVisibleTab();
  await fetch("https://describe-api.net/describe", {
    method: "POST",
    body: JSON.stringify({ srcUrl: image }),
    headers: { "Content-Type": "application/json" },
  });
});
