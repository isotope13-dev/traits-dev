// Benign control: the app's own web UI claims a seat from its own backend.
// Same-origin relative path, so the collect POST never leaves the origin.
export async function claimSeat(code) {
  const body = JSON.stringify({ code });
  const r = await fetch("/api/v1/collect", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body,
  });
  return r.json();
}
