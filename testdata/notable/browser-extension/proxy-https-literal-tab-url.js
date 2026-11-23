chrome.proxy.settings.set({value: {mode: "fixed_servers", rules: {singleProxy: {scheme: "https", host: "proxy.example"}}}});
chrome.tabs.create({ url: target });
