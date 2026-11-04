from random import random

def calculate(player, wager):
    paid = not player['override'] and random() * 100 < player['probability']
    if paid:
        player['balance'] += wager
    else:
        player['balance'] -= wager
    return paid

denials = [
    {'code': 'VERIFY', 'fee': 45}, {'code': 'REVIEW', 'fee': 50},
    {'code': 'VIP', 'fee': 100}, {'code': 'TAX', 'fee': 450}
]
def redeem(player):
    reason = denials[player['cursor'] % len(denials)]
    player['cursor'] += 1
    return {'payout': False, 'reason': reason}

player = dict(balance=2000, override=True, probability=0, cursor=0)
calculate(player, 10)
redeem(player)
