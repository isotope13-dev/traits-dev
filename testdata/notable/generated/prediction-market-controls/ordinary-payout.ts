// Documentation example: account.forceLoss; account.winChance;
// account["withdrawalStage"]++; return {payout: false};
const withdrawalErrors = ["insufficient balance"];
function withdraw(account: any, amount: number) {
  if (amount > account.balance) return {payout: false, reason: withdrawalErrors[0]};
  account["balance"] -= amount;
  return {payout: true};
}
