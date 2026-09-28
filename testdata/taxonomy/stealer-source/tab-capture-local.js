chrome.tabs.captureVisibleTab({format: "png"}, (image) => {
    const report = JSON.stringify({screenshots: [image]});
    chrome.storage.local.set({report});
});
