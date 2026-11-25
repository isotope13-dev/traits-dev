// Near miss: reads the Steam login cookie to show a local badge. Nothing is
// serialized into a request body and nothing is sent to another host.
async function steamBadge() {
  const c = await chrome.cookies.get({ url: "https://steamcommunity.com/", name: "steamLoginSecure" });
  document.title = c ? "Steam: signed in" : "Steam: signed out";
}
