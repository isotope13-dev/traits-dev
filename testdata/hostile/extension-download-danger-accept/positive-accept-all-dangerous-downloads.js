'use strict';
// Accepts Chrome's dangerous-download prompt for every download in the profile.
chrome.downloads.onChanged.addListener(delta => {
  const current = delta.danger && delta.danger.current;
  if (current && current !== 'safe' && current !== 'accepted') {
    chrome.downloads.acceptDanger(delta.id).catch(() => {});
  }
});
