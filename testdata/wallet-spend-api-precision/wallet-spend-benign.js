// Wallet SDK spend APIs: "send" moves funds signed by the key locally; the
// key, secret, seed, or mnemonic itself is never reported or transmitted.
// These must NOT read as credential-theft reporting calls.
export async function sendFromPrivateKey(api, privateKey, dest, amount) {
  const block = { account: dest, balance: amount };
  block.signature = await api.sign(privateKey, block);
  return api.process(block);
}

export async function sendFromPrivateKeyWithRepresentative(
  api,
  privateKey,
  dest,
  amount,
  representative,
) {
  const block = { account: dest, balance: amount, representative };
  block.signature = await api.sign(privateKey, block);
  return api.process(block);
}

export async function sendFromSecretKey(api, secretKey, dest, amount) {
  const block = { account: dest, balance: amount };
  block.signature = await api.sign(secretKey, block);
  return api.process(block);
}

export async function sendWithdrawalFromSeed(api, seed, seedIx, dest, amount) {
  const privateKey = api.derivePrivateKey(seed, seedIx);
  return sendFromPrivateKey(api, privateKey, dest, amount);
}

export async function sendBananoWithdrawalFromSeed(
  api,
  seed,
  dest,
  amount,
) {
  return sendWithdrawalFromSeed(api, seed, 0, dest, amount);
}

export async function sendWithdrawalFromMnemonic(api, mnemonic, dest, amount) {
  const seed = await api.mnemonicToSeed(mnemonic);
  return sendWithdrawalFromSeed(api, seed, 0, dest, amount);
}
