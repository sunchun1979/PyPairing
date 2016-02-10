import pandas
import ppGetMMS
import ppPenalty
import itertools
import random
import sys

import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)

def get_mutation(df, pos, finalPairing, currentIndex, currentSet, oppSet, total_round):
    if (not finalPairing):
        lowest = sys.maxint
    else:
        lowest = min(finalPairing, key=finalPairing.get)

    if (pos >= len(df)):
        penalty = ppPenalty.get_penalty(df, currentIndex, total_round)
        if (not finalPairing.has_key(penalty)):
            finalPairing[penalty] = []
        if (penalty>lowest):
            return
        finalPairing[penalty].append(currentIndex[:])
        return
    else:
        for p1 in range(0, len(df)):
            if (p1 not in currentSet):
                currentIndex.append(p1)
                currentSet.add(p1)
                for p2 in range(0, len(df)):
                    if (p2 not in currentSet):
                        if (df['id'][p2] not in oppSet[p1]):
                            currentIndex.append(p2)
                            currentSet.add(p2)
                            penalty = ppPenalty.get_penalty(df, currentIndex, total_round)
                            if (penalty<=lowest):
                                get_mutation(df, pos + 2, finalPairing, currentIndex, currentSet, oppSet, total_round)
                                currentIndex[pos], currentIndex[pos+1] = currentIndex[pos+1], currentIndex[pos]
                                get_mutation(df, pos + 2, finalPairing, currentIndex, currentSet, oppSet, total_round)
                                currentIndex[pos], currentIndex[pos+1] = currentIndex[pos+1], currentIndex[pos]
                            currentSet.remove(p2)
                            currentIndex.pop()
                currentSet.remove(p1)
                currentIndex.pop()
                return

def get_foldpairing(n):
    pairing = [None]*n
    if (n%4 != 0):
        mid = n/2-1
    else:
        mid = n/2
    for i in range(0,mid/2):
        pairing[2*i] = mid/2 + i
        pairing[2*i + 1] = i
    left = n - mid
    for i in range(0,left/2):
        pairing[2*i + mid] = mid + i + left/2
        pairing[2*i + 1 + mid] = mid + i
    return pairing

def generate_new_round(dframe, total_round, this_round):
    sortedFrame = ppGetMMS.sort_by_mms(dframe, False)
    oppset = []
    for i,item in sortedFrame['history'].iteritems():
        os=set()
        if (item!=""):
            for opp in item.split(";"):
                if (opp.lower() != 'bye'):
                    os.add(int(opp[1:-1]))
        oppset.append(os)

    finalPairing = {}
    currentIndex = []
    currentSet = set()
    finalList = []
    if (this_round == 0): #special treatment for the very first round for performance consideration
        first_pairing = get_foldpairing(len(sortedFrame))
        finalList.append((0, first_pairing))
    else:
        get_mutation(sortedFrame, 0, finalPairing, currentIndex, currentSet, oppset, total_round)
        topPairings = sorted(finalPairing.iteritems())[0]
        random.shuffle(topPairings[1])
        for item in topPairings[1]:
            finalList.append((topPairings[0], item))

    return finalList, sortedFrame
