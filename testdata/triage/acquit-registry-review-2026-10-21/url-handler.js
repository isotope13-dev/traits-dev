// Static scanner fixture. Never execute.
function openUrl(url) { return trySpawn("rundll32", ["url.dll,FileProtocolHandler", url]); }
