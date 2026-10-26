export async function accounts(provider, ethereum) {
  await provider.request({ method: "eth_accounts" });
  await ethereum.send("eth_accounts");
}
