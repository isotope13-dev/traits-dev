// Benign fixture: RLM direction marks inside a regex character class.
// Syncfusion-style RTL date-format separator detection: the marks are
// match alternatives for localized date strings, not spliced tokens.
export function dateSeparator(locale, sample) {
  var m = (sample || "").match(/[d‏M‏]([^d‏M])[d‏M‏]/i);
  return m ? m[1] : "/";
}
