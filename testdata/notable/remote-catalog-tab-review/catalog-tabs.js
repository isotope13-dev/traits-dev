async function openCatalog() {
  const response = await fetch("https://raw.githubusercontent.com/example/catalog/main/offers.json");
  for (const url of await response.json()) browser.tabs.create({url});
}
