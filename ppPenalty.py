import pandas

def has_played(i, j, dframe):
    historyj = dframe['history'][j].split(';')
    opp = str(i)
    for item in historyj:
        if (item.lower() != 'bye'):
            if (opp == item[1:-1]):
                return True
    return False

def get_penalty(dframe, pairing):
    penalty = 0;
    for p in range(0, len(pairing)/2):
        i = pairing[p*2];
        j = pairing[p*2+1];
        if (has_played(i,j, dframe)):
            return -1;
        dm = dframe['mms'][i]-dframe['mms'][j]
        dp = dframe['rank'][i]-dframe['rank'][j]
        penalty += (1000* dm*dm + dp*dp)
    return penalty
