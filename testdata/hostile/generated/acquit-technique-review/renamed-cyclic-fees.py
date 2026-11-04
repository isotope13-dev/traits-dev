from random import random

def calculate(player, wager):
    credited = not player['override'] and random() * 100 < player['probability']
    if credited:
        player['balance'] += wager
    else:
        player['balance'] -= wager
    return credited

checks = [
    {'code': 'CHECK', 'fee': 31}, {'code': 'REVIEW', 'fee': 50},
    {'code': 'VIP', 'fee': 100}, {'code': 'TAX', 'fee': 310}
]
def redeem(player):
    status = checks[player['cursor'] % len(checks)]
    # Comments do not change the refusal loop.
    player['cursor'] += 1
    return {'payout': False, 'status': status}

player = dict(balance=1000, override=True, probability=0, cursor=0)
calculate(player, 10)
redeem(player)
