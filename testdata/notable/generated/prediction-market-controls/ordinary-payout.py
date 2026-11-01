# Example: account['force_loss']; account['target_win_rate']
# account['withdrawal_step'] += 1
withdrawal_pretexts = ['insufficient balance']
def withdraw(account, amount):
    if amount > account['balance']:
        return {'payout': False, 'reason': withdrawal_pretexts[0]}
    account['balance'] -= amount
    return {'payout': True}
