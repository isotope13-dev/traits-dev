const label = "Disable other extension";
const explanation = "Another extension is controlling your proxy settings";
function onUserConfirm(id) {
  chrome.management.getAll().then(showExtensions);
  chrome.management.setEnabled(id, false);
  chrome.proxy.settings.set({value: {mode: "direct"}, scope: "regular"});
}
