async function readRequestedObjects(requestedIds, batchSize = 20) {
  const results = [];
  for (let index = 0; index < requestedIds.length; index += batchSize) {
    const id = requestedIds[index];
    const response = await fetch("https://catalog.corpus.invalid/api?id=" + id);
    if (response.ok) results.push(await response.json());
  }
  return results;
}
