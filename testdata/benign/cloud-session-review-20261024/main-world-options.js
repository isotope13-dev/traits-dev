const options = { world: "MAIN" };
chrome.scripting.executeScript(options);
browser.scripting.executeScript({world: browser.scripting.ExecutionWorld.MAIN});
