import pandas
import itertools
import ppIO
import ppGenRound
import ppUpdateRound
import ppGetMMS
import random
import sys

def gen_winner(match_name):
    match_name['Result'] = pandas.Series(len(match_name), index=match_name.index)
    for i in range(0,len(match_name)):
        pick = random.randint(0,1)
        match_name.set_value(i,['Result'], match_name.loc[i][pick])
    return match_name

# beginning of main entry

#testCases = ['Test_Case1.txt', 'Test_Case2.txt', 'Test_Case3.txt']
testCases = ['Test_Case1.txt']
totalRound = 4

for tFile in testCases:
    dfRound, handicapInfo = ppIO.read_round(tFile)
    for trial in range(0,1):
        resultFile = tFile.replace(".txt", "_Result_" + str(trial) + ".txt")
        sys.stdout = open(resultFile, 'w')
        for r in range(0,totalRound):
            for i in range(0,len(dfRound)):
                if (handicapInfo[i]==1):
                    handicapTxt = "(Handicap)"
                else:
                    handicapTxt = ""
                print "[Section " + str(i+1) + "]" + handicapTxt + ": Position before round " + str(r+1) + ":"
                print dfRound[i]
            print "\n"
            for i in range(0, len(dfRound)):
                finalPairing, sortedFrame = ppGenRound.generate_new_round(dfRound[i], totalRound, r)
                #print finalPairing[0]
                resTable = ppIO.print_pairing(finalPairing[0][1], dfRound[i])
                result = gen_winner(resTable)
                print "\nResult after round " + str(r+1) + ":"
                print result
                dfRound[i] = ppUpdateRound.update_round(sortedFrame, result)
                dfRound[i] = ppGetMMS.sort_by_mms(dfRound[i], False)
                print "\nStanding after round " + str(r+1) + ":"
                print dfRound[i]
                dfRound[i].drop(['mms','soms','sodms'],1)
            print "\n=======\n"


