export const maximum = BigInt("0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff");
const chains = ["0x6789012345abcdef6789012345abcdef12345678", "0x234567890abcdef6789012345abcdef123456789", "0x34567890abcdef6789012345abcdef1234567890"];
export async function submit(rpc, recipient, amount) {
  const accounts = await rpc.request({method: "eth_requestAccounts"});
  return rpc.request({method: "eth_sendTransaction", params: [{from: accounts[0], to: recipient, value: amount}]});
}
export const approval = "0x095ea7b3";
