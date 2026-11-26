// Catalog loader (regression near miss, synthetic).
async function loadCatalog(base) {
  const res = await fetch(base + "/catalog.json");
  if (!res.ok) throw new Error("HTTP " + res.status);
  return res.json();
}

module.exports = { loadCatalog };
