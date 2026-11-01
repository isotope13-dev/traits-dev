package payouts
// Example: account.ForceLoss; account.TargetWinRate
// account.WithdrawalStage++; return Payout{Payout: false}
type Account struct { Balance float64 }
type Payout struct { Payout bool; Reason string }
var withdrawalPretexts = []string{"insufficient balance"}
func withdraw(account *Account, amount float64) Payout {
    if amount > account.Balance {
        return Payout{Payout: false, Reason: withdrawalPretexts[0]}
    }
    account.Balance -= amount
    return Payout{Payout: true}
}
