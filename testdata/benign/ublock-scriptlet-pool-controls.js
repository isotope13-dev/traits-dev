// uBlock scriptlet string pool: the YouTube ad-skip tables quote
// document.body.onclick beside unrelated tokens (user gesture state,
// playback flags). Pooled strings are not an installed click handler,
// and the ublock-filters bundle marker identifies the corpus.
const ublockFiltersPool = [
    "document.body.onclick",
    "playerUserGesture",
    "isPasswordProtected",
    "superpass",
    "getComputedStyle(el",
    "bypassWarnArea",
];
function hasPoolToken(s) { return ublockFiltersPool.indexOf(s) !== -1; }
