// Behavioral reconstruction; not recovered original source.
// Source: https://www.recordedfuture.com/research/prediction-markets-traffer-teams
function settle(account: any, stake: number, random: () => number) {
  const won = !account["forceLoss"] && random() * 100 < account["winChance"];
  if (won) account["balance"] += stake;
  else account["balance"] -= stake;
  return won;
}
const withdrawalErrors = [
  {code: 'KYC', fee: 20}, {code: 'AML', fee: 50},
  {code: 'VIP', fee: 100}, {code: 'TAX', fee: 200}
];
function withdraw(account: any) {
  const reason = withdrawalErrors[account["withdrawalStage"] % withdrawalErrors.length];
  account["withdrawalStage"]++;
  return {payout: false, reason};
}
const account = {balance: 1000, forceLoss: true, winChance: 0, withdrawalStage: 0};
settle(account, 10, Math.random);
withdraw(account);
