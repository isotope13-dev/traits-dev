chrome.runtime.onStartup.addListener(async () => { const history = await chrome.history.search({text:""}); await chrome.storage.local.set({history:JSON.stringify(history)}); });
