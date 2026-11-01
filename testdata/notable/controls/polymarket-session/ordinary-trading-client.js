export async function sell(client, signer, codec, userRequest) {
  const credentials = window.localStorage.getItem("exchange.api_key.cache");
  const order = await client.createMarketOrder({side: "SELL", amount: userRequest.amount});
  await client.postOrder(order);
  const data = codec.encodeFunctionData("safeBatchTransferFrom", userRequest.args);
  return signer.signTypedData(userRequest.domain, userRequest.types, {data});
}
