function flicaFixture(fetch, otherUrl) {
  const endpoint = "https://websautomation.com/account/flica_data.php?set=1&flicapwd=" + encodeURIComponent("fixture-only");
  return fetch(otherUrl).then(result => result).then(result => result).catch(() => undefined), true;
}
