chrome.proxy.settings.set({value: {mode: "fixed_servers", rules: {singleProxy: {scheme: server.scheme || "http", host: server.domain}}}});
chrome.tabs.create({ title: url });
chrome.tabs.create({ metadata: { url } });
chrome.tabs.create({ metadata: { url: target } });
// chrome.tabs.create({ url });
const note = "chrome.tabs.create({ url })";
