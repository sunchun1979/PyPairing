import pandas
import ppGetMMS
import ppPenalty
import itertools
import random
import sys

import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)

def get_mutation(df, pos, finalPairing, currentIndex, currentSet, oppSet, totalCount):
    if (not finalPairing):
        lowest = sys.maxint
    else:
        lowest = min(finalPairing, key=finalPairing.get)
    N = len(df)
    # only approximation for large groups; performance concern
    if (N>12 and totalCount[0]>N*(N-1)*(N-2)):
        return

    if (pos >= N):
        penalty = ppPenalty.get_penalty(df, currentIndex)
        if (not finalPairing.has_key(penalty)):
            finalPairing[penalty] = []
        if (penalty>lowest):
            return
        finalPairing[penalty].append(currentIndex[:])
        totalCount[0] += 1
        return
    else:
        for p1 in range(0, N):
            if (p1 not in currentSet):
                currentIndex.append(p1)
                currentSet.add(p1)
                for p2 in range(0, N):
                    if (p2 not in currentSet):
                        if (df['id'][p2] not in oppSet[p1]):
                            currentIndex.append(p2)
                            currentSet.add(p2)
                            penalty = ppPenalty.get_penalty(df, currentIndex)
                            if (penalty<=lowest):
                                get_mutation(df, pos + 2, finalPairing, currentIndex, currentSet, oppSet, totalCount)
                                currentIndex[pos], currentIndex[pos+1] = currentIndex[pos+1], currentIndex[pos]
                                get_mutation(df, pos + 2, finalPairing, currentIndex, currentSet, oppSet, totalCount)
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

def generate_new_round(dframeList, currentBand, this_round, handicap = False):
    dframe = dframeList[currentBand]
    sortedFrame = ppGetMMS.sort_by_mms(dframeList, currentBand, False, handicap)
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
        totalCount = [0]
        get_mutation(sortedFrame, 0, finalPairing, currentIndex, currentSet, oppset, totalCount)
        topPairings = sorted(finalPairing.iteritems())[0]
        random.shuffle(topPairings[1])
        for item in topPairings[1]:
            finalList.append((topPairings[0], item))

    return finalList, sortedFrame
