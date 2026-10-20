async function resetOwnStorage() {
  const databases = await indexedDB.databases();
  databases.forEach(({name}) => indexedDB.deleteDatabase(name));
}
