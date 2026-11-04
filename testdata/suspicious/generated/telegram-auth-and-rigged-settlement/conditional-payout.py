from random import random

def settle(account, stake):
    won = not account['force_loss'] and random() * 100 < account['target_win_rate']
    if won:
        account['balance'] += stake
    else:
        account['balance'] -= stake
    return won

withdrawal_pretexts = [
    {'code': 'KYC', 'fee': 20}, {'code': 'AML', 'fee': 50},
    {'code': 'VIP', 'fee': 100}, {'code': 'TAX', 'fee': 200}
]
def withdraw(account):
    reason = withdrawal_pretexts[account['withdrawal_step'] % len(withdrawal_pretexts)]
    account['withdrawal_step'] += 1
    if account['balance'] <= 0:
        return {'payout': False, 'reason': reason}
    return {'payout': True}

account = dict(balance=1000, force_loss=True, target_win_rate=0, withdrawal_step=0)
settle(account, 10)
withdraw(account)
