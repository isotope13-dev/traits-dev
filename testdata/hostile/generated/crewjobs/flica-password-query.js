function flicaFixture(fetch) {
  const endpoint = "https://websautomation.com/account/flica_data.php?set=1&flicapwd=" + encodeURIComponent("fixture-only");
  return fetch(endpoint).then(result => result).then(result => result).catch(() => undefined), true;
}
