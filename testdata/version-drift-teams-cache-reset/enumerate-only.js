chrome.scripting.executeScript({target: {tabId: 12}, func: async () => {
  return await indexedDB.databases();
}});
