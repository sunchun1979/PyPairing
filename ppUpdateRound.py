def update_round(dframe, previous):
    ndict = {}
    for i in range(0, len(dframe)):
        ndict[dframe['name'][i]] = i
    for i in range(0, len(previous)):
        win = ndict[previous['Result'][i]]
        if (previous['Result'][i] == previous['Black'][i]):
            c = 'B'
            loss = ndict[previous['White'][i]]
        else:
            c = 'W'
            loss = ndict[previous['Black'][i]]
        dframe.set_value(win, 'history', dframe['history'][win] + ';' + c + str(dframe['id'][loss]) + '+')
        dframe.set_value(loss, 'history', dframe['history'][loss] + ';' + c + str(dframe['id'][win]) + '-')
    return dframe
