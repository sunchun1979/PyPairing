def get_wins(history):
    wins = 0; loss = 0; bye = 0;
    for item in history.split(';'):
        if "+" in item:
            wins += 1
        elif "-" in item:
            loss += 1
        else:
            bye += 1
    return wins + bye * 0.5


def get_mms(rank, history):
    return rank + get_wins(history)