import pandas

def get_penalty(dframe, pairing, total_round):
    penalty = 0;
    for p in range(0, len(pairing)/2):
        i = pairing[p*2];
        j = pairing[p*2+1];
        dm = dframe['mms'][i]-dframe['mms'][j]
        dp = dframe['rank'][i]-dframe['rank'][j]
        iw = dframe['history'][i].upper().count('W')
        ib = dframe['history'][i].upper().count('B') - dframe['history'][i].upper().count('y')
        jw = dframe['history'][j].upper().count('W')
        jb = dframe['history'][j].upper().count('B') - dframe['history'][j].upper().count('y')
        ic = iw-ib
        jc = jw-jb
        dr = abs(i-j)-(total_round)
        penalty += (10000 * dm*dm + 100 * dp*dp + 10 * dr*dr + ic*ic + jc*jc)
    return penalty
