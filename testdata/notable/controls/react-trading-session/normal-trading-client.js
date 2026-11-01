export async function trade(client, signer, abi, args, domain, types, message) {
  if (typeof client.postOrder === "function" && typeof client.createOrder === "function") {
    await client.postOrder(await client.createOrder(args));
    abi.encodeFunctionData("safeBatchTransferFrom", args);
    return signer.signTypedData(domain, types, message);
  }
}
