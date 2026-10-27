chrome.management.getAll().then(extensions => {
  extensions.forEach(extension => {
    if (extension.permissions.includes("proxy"))
      chrome.management.setEnabled(extension.id, false);
  });
  chrome.proxy.settings.set({value: {mode: "direct"}, scope: "regular"});
});
