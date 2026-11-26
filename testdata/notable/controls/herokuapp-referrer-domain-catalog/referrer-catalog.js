// Analytics referrer classification: search-engine domain catalog.
var searchDomains = "google.com|consent.google.co.uk|py-google.herokuapp.com|translate.google.co.jp|bing.com";
function isSearchReferrer(host) {
  return searchDomains.split("|").indexOf(host) !== -1;
}
