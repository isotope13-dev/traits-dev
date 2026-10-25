chrome.permissions.request({origins: ["https://example.org/*"]});
browser.permissions.remove({permissions: ["tabs"]});
window.browser.permissions.contains({permissions: ["downloads"]});
