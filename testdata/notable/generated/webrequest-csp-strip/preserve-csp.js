chrome.webRequest.onHeadersReceived.addListener(details => {
  return {responseHeaders: details.responseHeaders.filter(h =>
    h.name.toLowerCase() !== 'x-debug-token')};
}, {urls: ['<all_urls>']}, ['blocking', 'responseHeaders']);
