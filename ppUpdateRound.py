def update_round(dframe, previous):
    ndict = {}
    for i in range(0, len(dframe)):
        ndict[dframe['name'][i]] = i
    for i in range(0, len(previous)):
        if (not previous['Result'][i] in ndict): continue
        win = ndict[previous['Result'][i]]
        if (previous['Result'][i] == previous['Black'][i]):
            c = 'B'
            loss = ndict[previous['White'][i]]
        else:
            c = 'W'
            loss = ndict[previous['Black'][i]]
        if (dframe['history'][win]!=""):
            delim = ';'
        else:
            delim = ''
        dframe.set_value(win, 'history', dframe['history'][win] + delim + c + str(dframe['id'][loss]) + '+')
        if (dframe['history'][loss]!=""):
            delim = ';'
        else:
            delim = ''
        dframe.set_value(loss, 'history', dframe['history'][loss] + delim + c + str(dframe['id'][win]) + '-')
    return dframe
