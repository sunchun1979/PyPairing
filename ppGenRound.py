import pandas
import ppGetMMS
import ppPenalty
from collections import OrderedDict
import itertools

def get_mutation(df, pos, finalPairing, currentIndex, currentSet, oppSet):
    if (pos >= len(df)):
        #print currentIndex
        #print ppPenalty.get_penalty(df,currentIndex)
        #finalPairing.append( (currentIndex[:], ppPenalty.get_penalty(df, currentIndex)))
        penalty = ppPenalty.get_penalty(df, currentIndex)
        if (not finalPairing.has_key(penalty)):
            finalPairing[penalty] = []
        finalPairing[penalty].append(currentIndex[:])
        return
    else:
        for p1 in range(0, len(df)):
            if (p1 not in currentSet):
                currentIndex.append(p1)
                currentSet.add(p1)
                #get_mutation(df, pos + 1, finalPairing, currentIndex, currentSet, oppSet)
                for p2 in range(0, len(df)):
                    if (p2 not in currentSet):
                        if (p2 not in oppSet[p1]):
                            currentIndex.append(p2)
                            currentSet.add(p2)
                            get_mutation(df, pos + 2, finalPairing, currentIndex, currentSet, oppSet)
                            currentSet.remove(p2)
                            currentIndex.pop()
                currentSet.remove(p1)
                currentIndex.pop()
                return
        # else:
        #     for p1 in range(0, len(df)):
        #         if (p1 not in currentSet):
        #             if (p1 not in oppSet[currentIndex[pos-1]]):
        #                 currentIndex.append(p1)
        #                 currentSet.add(p1)
        #                 get_mutation(df, pos + 1, finalPairing, currentIndex, currentSet, oppSet)
        #                 currentSet.remove(p1)
        #                 currentIndex.pop()
        # return


def generate_new_round(dframe):
    dframe['mms'] = pandas.Series.from_array(dframe['rank'])
    for i, row in dframe['mms'].iteritems():
        dframe['mms'].set_value(i, ppGetMMS.get_mms(dframe['rank'][i], dframe['history'][i]))
    sortedIndex = dframe['mms'].sort_values(ascending=True).index
    sortedFrame = dframe.reindex(sortedIndex).reset_index(drop=True)
    oppset = []
    for i,item in dframe['history'].iteritems():
        os=set()
        if (item!=""):
            if (item.lower() != 'bye'):
                os.add(int(item[1:-1]))
        oppset.append(os)

    print sortedFrame
    finalPairing = OrderedDict()
    currentIndex = []
    currentSet = set()
    get_mutation(sortedFrame, 0, finalPairing, currentIndex, currentSet, oppset)
    finalList = []
    for k,v in finalPairing.iteritems():
        for item in v:
            finalList.append((k, item))

    return finalList
