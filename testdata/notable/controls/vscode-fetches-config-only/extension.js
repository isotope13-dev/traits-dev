async function checkForUpdate() {
  const config = await (await fetch('https://updates.example.invalid/config.json')).json();
  return config.latest_version;
}
module.exports = { activate: checkForUpdate };
