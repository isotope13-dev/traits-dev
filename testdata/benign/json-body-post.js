// Benign control for json-body-post: an ordinary event-capture POST with a
// serialized JSON body. The neutral composite must fire; no install-hook
// context exists here.
async function sendEvent(url, event) {
  const body = JSON.stringify(event);
  await fetch(url, { method: "POST", body });
}
