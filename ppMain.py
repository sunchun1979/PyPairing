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

#testCases = ['Test_Case2.txt']
testCases = ['Test_Case1.txt']
totalRound = 4

# Generate Test Cases
for tFile in testCases:
    for trial in range(0,10):
        dfRound, handicapInfo = ppIO.read_round(tFile)
        resultFile = tFile.replace(".txt", "_Result_" + str(trial) + ".txt")
        sys.stdout = open(resultFile, 'w')

        # Actual Logic
        for r in range(0,totalRound):
            print "[=== ROUND " + str(r+1) + " ===]"
            print "Position before round " + str(r+1) + ":"
            for i in range(0,len(dfRound)-1):
                if (handicapInfo[i]):
                    handicapTxt = "(Handicap)"
                else:
                    handicapTxt = ""
                print "[Section " + str(i+1) + "]" + handicapTxt + ":"
                print dfRound[i]

            # simulating random events of two people take bye
            # this part should be done manually in real life
            # we have 20% chance of two people taking bye.
            # if single people took bye, opponent receive a Bye (manual) and a unrated fast game with TD
            if (r!=0 and random.random()<0):
                print " ** RE-BANDING ** "

                #random band, random player
                rnd_band = random.randint(0,len(dfRound)-2)
                band_index = random.randint(0,len(dfRound[rnd_band])-1)
                dfRound[-1].loc[len(dfRound[-1])] = dfRound[rnd_band].loc[band_index]
                dfRound[rnd_band].drop(dfRound[rnd_band].index[[band_index]],inplace=True)
                dfRound[rnd_band] = dfRound[rnd_band].reset_index(drop=True)
                #twice
                rnd_band = random.randint(0,len(dfRound)-2)
                band_index = random.randint(0,len(dfRound[rnd_band])-1)
                dfRound[-1].loc[len(dfRound[-1])] = dfRound[rnd_band].loc[band_index]
                dfRound[rnd_band].drop(dfRound[rnd_band].index[[band_index]],inplace=True)
                dfRound[rnd_band] = dfRound[rnd_band].reset_index(drop=True)

                # get the top player from next section
                for i in range(0,len(dfRound)-2):
                    if (len(dfRound[i])%2==1):
                        dfRound[i].loc[len(dfRound[i])] = dfRound[i+1].loc[0]
                        dfRound[i+1].drop(dfRound[i+1].index[0],inplace=True)
                        dfRound[i] = dfRound[i].reset_index(drop=True)
                        dfRound[i+1] = dfRound[i+1].reset_index(drop=True)

                for i in range(0,len(dfRound)-1):
                    if (handicapInfo[i]):
                        handicapTxt = "(Handicap)"
                    else:
                        handicapTxt = ""
                    print "[Section " + str(i+1) + "]" + handicapTxt + ":"
                    print dfRound[i]
                print "[Section Bye]"
                print dfRound[-1]

            allResults = []
            allStanding = []
            allPairing = []
            allSortedFrame = []

            for i in range(0, len(dfRound)-1):
                finalPairing, sortedFrame = ppGenRound.generate_new_round(dfRound, i,  r, handicapInfo[i])
                allPairing.append(finalPairing)
                allSortedFrame.append(sortedFrame)

            for i in range(0, len(dfRound)-1):
                finalPairing = allPairing[i]
                resTable = ppIO.print_pairing(finalPairing[0][1], allSortedFrame[i], handicapInfo[i])
                result = gen_winner(resTable)
                allResults.append(result)
            print "Round " + str(r+1) + " results:"
            for item in allResults:
                print item

            for i in range(0, len(dfRound)-1):
                sortedFrame = allSortedFrame[i]
                result = allResults[i]
                dfRound[i] = ppUpdateRound.update_round(sortedFrame, result)
                dfRound[i] = ppGetMMS.sort_by_mms(dfRound, i, dropAux=False, handicap=handicapInfo[i])
                allStanding.append(dfRound[i].copy())
            print "Round " + str(r+1) + " standing:"
            for item in allStanding:
                print item

            for i in range(0, len(dfRound)-1):
                dfRound[i].drop(['mms','soms','sodms'],1,inplace=True)

            print "\n"


