document.getElementById("reset").addEventListener("click", async () => {
  await chrome.scripting.executeScript({target: {tabId: 12}, world: "MAIN", func: async () => {
    const databases = await indexedDB.databases();
    databases.forEach(({name}) => indexedDB.deleteDatabase(name));
  }});
});
