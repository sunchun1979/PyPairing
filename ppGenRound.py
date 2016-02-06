import pandas


def get_wins(history):
    return 1


def get_mutation(df, pos, finalPairing, currentIndex, currentSet):
    if (pos >= len(df)):
        print currentIndex
        finalPairing.append(currentIndex[:])
        return
    else:
        for p1 in range(0, len(df)):
            if (p1 in currentSet):
                continue
            if (pos % 2 == 1):
                if (p1 < currentIndex[pos-1]):
                    continue
            currentIndex.append(p1)
            currentSet.add(p1)
            get_mutation(df, pos + 1, finalPairing, currentIndex, currentSet)
            currentSet.remove(p1)
            currentIndex.pop()
        return


def generate_new_round(dframe):
    dframe['score'] = dframe['rank']
    score = pandas.Series.from_array(dframe['score'])
    for i, row in score.iteritems():
        score.set_value(i, row + get_wins(dframe['history'][i]))
    sortedIndex = score.sort_values(ascending=True).index
    sortedFrame = dframe.reindex(sortedIndex).reset_index(drop=True)
    print sortedFrame
    finalPairing = []
    currentIndex = []
    currentSet = set()
    get_mutation(sortedFrame, 0, finalPairing, currentIndex, currentSet)
    print finalPairing
