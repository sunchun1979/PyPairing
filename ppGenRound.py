import pandas
import ppGetMMS
import ppPenalty
import itertools

def get_mutation(df, pos, finalPairing, currentIndex, currentSet, oppSet, total_round):
    if (pos >= len(df)):
        penalty = ppPenalty.get_penalty(df, currentIndex, total_round)
        if (not finalPairing.has_key(penalty)):
            finalPairing[penalty] = []
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
                            get_mutation(df, pos + 2, finalPairing, currentIndex, currentSet, oppSet, total_round)
                            currentIndex[pos], currentIndex[pos+1] = currentIndex[pos+1], currentIndex[pos]
                            get_mutation(df, pos + 2, finalPairing, currentIndex, currentSet, oppSet, total_round)
                            currentIndex[pos], currentIndex[pos+1] = currentIndex[pos+1], currentIndex[pos]
                            currentSet.remove(p2)
                            currentIndex.pop()
                currentSet.remove(p1)
                currentIndex.pop()
                return

def generate_new_round(dframe, total_round, this_round):
    dframe['mms'] = pandas.Series.from_array(dframe['rank'])
    for i, row in dframe['mms'].iteritems():
        dframe['mms'].set_value(i, ppGetMMS.get_mms(dframe['rank'][i], dframe['history'][i]))
    sortedFrame = dframe.sort(['mms']).reset_index(drop=True)
    oppset = []
    for i,item in sortedFrame['history'].iteritems():
        os=set()
        if (item!=""):
            for opp in item.split(";"):
                if (opp.lower() != 'bye'):
                    os.add(int(opp[1:-1]))
        oppset.append(os)

    print sortedFrame
    finalPairing = {}
    currentIndex = []
    currentSet = set()
    get_mutation(sortedFrame, 0, finalPairing, currentIndex, currentSet, oppset, total_round)
    finalList = []
    for k,v in sorted(finalPairing.iteritems()):
        for item in v:
            finalList.append((k, sortedFrame['id'].reindex(item).tolist()))

    return finalList
