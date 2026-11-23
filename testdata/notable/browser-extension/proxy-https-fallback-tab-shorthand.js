chrome.proxy.settings.set({value: {mode: "fixed_servers", rules: {singleProxy: {scheme: server.scheme || "https", host: server.domain}}}});
chrome.tabs.create({ url });
browser.tabs.create({ active: true, url });
chrome.tabs.create({ url: target });
