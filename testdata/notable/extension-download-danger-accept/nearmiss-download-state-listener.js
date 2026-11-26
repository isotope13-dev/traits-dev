'use strict';
// Logs download state changes for the course-material queue; accepts nothing.
chrome.downloads.onChanged.addListener(delta => {
  if (delta.state && delta.state.current === 'complete') {
    console.log('course file ready', delta.id);
  }
});
