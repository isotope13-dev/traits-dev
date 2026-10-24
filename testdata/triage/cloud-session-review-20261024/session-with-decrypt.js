async function inspectSession() {
  const getRecord = (dbName, storeName, key) => new Promise((resolve) => {
    const request = indexedDB.open(dbName);
    request.onsuccess = () => {
      const record = request.result.transaction(storeName, "readonly").objectStore(storeName).get(key);
      record.onsuccess = () => resolve(record.result);
    };
  });
  const key = (await getRecord("wawc_db_enc", "keys", 1)).key;
  const info = JSON.parse(localStorage.getItem("WANoiseInfo"));
  const signal_reg_id = 1;
  return crypto.subtle.decrypt({name: "AES-CBC", iv: info.iv}, key, info.privKey);
}
