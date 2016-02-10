import pandas
import itertools
import ppIO
import ppGenRound
import ppUpdateRound
import ppGetMMS
import random

def gen_winner(match_name):
    match_name['Result'] = pandas.Series(len(match_name), index=match_name.index)
    for i in range(0,len(match_name)):
        pick = random.randint(0,1)
        match_name.set_value(i,['Result'], match_name.loc[i][pick])
    return match_name

# beginning of main entry

dfRound = ppIO.read_round("Test_Case1.txt")
print dfRound

totalRound = 4
for i in range(0,totalRound):
    finalPairing, sortedFrame = ppGenRound.generate_new_round(dfRound, totalRound, i)
    print finalPairing[0]
    resTable = ppIO.print_pairing(finalPairing[0][1], dfRound)
    result = gen_winner(resTable)
    print result
    dfRound = ppUpdateRound.update_round(sortedFrame, result)
    dfRound = ppGetMMS.sort_by_mms(dfRound, False)
    print dfRound
    dfRound.drop(['mms'],1)


