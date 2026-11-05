const flags = ["--disable-blink-features=AutomationControlled"];
chromium.launch({args: flags, ignoreDefaultArgs: ["--enable-automation"]});
