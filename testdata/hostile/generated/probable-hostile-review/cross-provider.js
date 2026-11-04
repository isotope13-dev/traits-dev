chrome.declarativeNetRequest.updateDynamicRules({
  addRules: [{id: 1, action: {type: "redirect", redirect: {
    regexSubstitution: "https://search.yahoo.com/yhs/search?hspart=example&p=\\1"
  }}, condition: {regexFilter: ".*\\/search\\?q=(.*)$", resourceTypes: ["main_frame"]}}],
  removeRuleIds: [1]
});
