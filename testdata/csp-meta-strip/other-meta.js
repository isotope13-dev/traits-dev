chrome.webRequest.onHeadersReceived.addListener(details => ({
  responseHeaders: details.responseHeaders.filter(header => header.name.toLowerCase() !== "content-security-policy")
}), {urls: ["<all_urls>"]}, ["blocking", "responseHeaders"]);
function clearPolicy() {
  document.querySelectorAll('meta[http-equiv="refresh"]').forEach(node => node.remove());
}
clearPolicy();
new MutationObserver(clearPolicy).observe(document.documentElement, {childList: true, subtree: true});
