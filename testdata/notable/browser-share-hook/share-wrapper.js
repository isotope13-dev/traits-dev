var browser = window;
var originalShare = browser.navigator.share.bind(browser.navigator);
browser.navigator.share = function (data) {
  data.text = String(data.text).trim();
  return originalShare(data);
};
