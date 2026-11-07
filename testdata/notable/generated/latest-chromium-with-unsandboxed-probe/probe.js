const browser = {resolveBuildId:async(platform, version="latest")=>version};
console.log("Chromium revision:");
launchBrowser.launch({headless:"new",args:["--no-sandbox"],executablePath:browser.executablePath});
