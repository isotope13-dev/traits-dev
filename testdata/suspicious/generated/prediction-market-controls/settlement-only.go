package main

import "math/rand"

type Account struct {
    Balance float64
    ForceLoss bool
    TargetWinRate float64
    WithdrawalStage int
}
type Refusal struct { Code string; Fee float64 }
type Payout struct { Payout bool; Reason Refusal }
var withdrawalPretexts = []Refusal{
    {"KYC", 20}, {"AML", 50}, {"VIP", 100}, {"TAX", 200},
}
func settle(account *Account, stake float64) bool {
    won := !account.ForceLoss && rand.Float64()*100 < account.TargetWinRate
    if won { account.Balance += stake } else { account.Balance -= stake }
    return won
}
