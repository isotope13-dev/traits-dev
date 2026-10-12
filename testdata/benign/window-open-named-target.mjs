// Positive control: global open() of a computed URL into a named window.
// Must still fire open-computed-url-named-target.
export function openHelpPanel(url) {
  open(url, "help-panel");
}
