import pandas

def get_wins(history):
    wins = 0; loss = 0; bye = 0;
    for item in history.split(';'):
        if (item == ""):
            continue
        if "+" in item:
            wins += 1
        elif "-" in item:
            loss += 1
        else:
            bye += 1
    return wins + bye * 0.5

def get_mms(rank, history, handicap=False):
    if (handicap):
        return get_wins(history)
    else:
        return rank + get_wins(history)

def get_soms(mms, history):
    soms = 0
    for item in history.split(';'):
        if (item == ""):
            continue
        if (item.lower()!="bye"):
            opp = int(item[1:-1])
            soms = soms + mms[opp]
    return soms

def get_sodms(mms, history):
    sodms = 0
    for item in history.split(';'):
        if (item == ""):
            continue
        if (item.lower()!="bye"):
            if ("+" in item):
                opp = int(item[1:-1])
                sodms = sodms + mms[opp]
    return sodms

def sort_by_mms(dframeList, currentBand, dropAux = True, handicap = False):
    mms = {}
    for j in range(0, len(dframeList)):
        dframeList[j]['mms'] = pandas.Series(0, index=dframeList[j].index)
        dframeList[j]['soms'] = pandas.Series(0, index=dframeList[j].index)
        dframeList[j]['sodms'] = pandas.Series(0, index=dframeList[j].index)
        for i, row in dframeList[j]['mms'].iteritems():
            dframeList[j]['mms'].set_value(i, get_mms(dframeList[j]['rank'][i], dframeList[j]['history'][i], handicap))
        for i in range(0,len(dframeList[j])):
            mms[dframeList[j]['id'][i]] = dframeList[j]['mms'][i]
    for j in range(0, len(dframeList)):
        for i, row in dframeList[j]['soms'].iteritems():
            dframeList[j]['soms'].set_value(i, get_soms(mms, dframeList[j]['history'][i]))
        for i, row in dframeList[j]['sodms'].iteritems():
            dframeList[j]['sodms'].set_value(i, get_sodms(mms, dframeList[j]['history'][i]))
        dframeList[j] = dframeList[j].sort(['mms','soms','sodms'],ascending=[False, False, False]).reset_index(drop=True)
        if (dropAux):
            dframeList[j] = dframeList[j].drop(['mms','soms','sodms'],1)

    return dframeList[currentBand]
    # dframe = dframeList[currentBand]
    # dframe['mms'] = pandas.Series(0, index=dframe.index)
    # dframe['soms'] = pandas.Series(0, index=dframe.index)
    # dframe['sodms'] = pandas.Series(0, index=dframe.index)
    # for i, row in dframe['mms'].iteritems():
    #     dframe['mms'].set_value(i, get_mms(dframe['rank'][i], dframe['history'][i], handicap))
    # mms = {}
    # for i in range(0,len(dframe)):
    #     mms[dframe['id'][i]] = dframe['mms'][i]
    # # for j in range(0, len(dframeList)):
    # #     for i in range(0, len(dframeList[j])):
    # #         mms[dframeList[j]['id'][i]] = dframeList[j]['mms'][i]
    # for i, row in dframe['soms'].iteritems():
    #     dframe['soms'].set_value(i, get_soms(mms, dframe['history'][i]))
    # for i, row in dframe['sodms'].iteritems():
    #     dframe['sodms'].set_value(i, get_sodms(mms, dframe['history'][i]))
    # dframe = dframe.sort(['mms','soms','sodms'],ascending=[False, False, False]).reset_index(drop=True)
    # if (dropAux):
    #     dframe = dframe.drop(['mms','soms','sodms'],1)
    # return dframe
