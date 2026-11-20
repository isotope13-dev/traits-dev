const settings = Storage.prototype;
const old = settings.setItem;
const tabId = 1;
chrome.debugger.attach({tabId}, '1.3');
chrome.debugger.sendCommand({tabId}, 'Network.getAllCookies');
sessionStorage.setItem('theme', 'dark');
document.addEventListener('keydown', e => {
  if (e.ctrlKey && e.key === 's') saveDocument();
}, true);
document.addEventListener('paste', e => {
  editor.insertText(e.clipboardData.getData('text/plain'));
}, true);
log(`[INFO]${status}[/INFO]`);
