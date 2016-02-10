import pandas
import itertools
import ppIO
import ppGenRound
import ppUpdateRound
import random

def gen_winner(match_name):
    match_name['Result'] = pandas.Series(len(match_name), index=match_name.index)
    for i in range(0,len(match_name)):
        pick = random.randint(0,1)
        match_name.set_value(i,['Result'], match_name.loc[i][pick])
        #match_name.loc[len(match_name)] = [match_name.loc[i][pick], match_name.loc[i][1-pick]]
    return match_name

dfRound = ppIO.read_round("Round0b.txt")
print dfRound
finalPairing, sortedFrame = ppGenRound.generate_new_round(dfRound, 4, 1)
# for pair in finalPairing:
#     print pair
print finalPairing[0]
resTable = ppIO.print_pairing(finalPairing[0][1], sortedFrame)
print resTable

result = gen_winner(resTable)
print result
dfRoundNew = ppUpdateRound.update_round(dfRound, result)
print dfRoundNew


