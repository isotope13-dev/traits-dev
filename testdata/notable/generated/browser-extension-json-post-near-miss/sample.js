// Send a text search query to the vendor's search API.
async function search(query) {
  const r = await fetch("https://api.example-search.test/query", {
    method: "POST",
    body: JSON.stringify({ query }),
    headers: { "Content-Type": "application/json" },
  });
  return r.json();
}
