function renderTrustedMath(parser, url) {
    if (!parser.settings.isTrusted({command: "url", url})) return;
}
function createTerminalAnnouncement(node) {
    node.setAttribute("aria-live", "assertive");
}
