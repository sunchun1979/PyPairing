import csv
import pandas

def read_round(filename):
    rawframe = pandas.read_csv(filename)
    rawframe = rawframe.fillna("")
    dframe = []
    handicapInfo = [False]
    begin = 0
    for i in range(0,len(rawframe)):
        if (rawframe['id'][i]=='='):
            dframe.append(rawframe.loc[begin:i-1].reset_index(drop=True))
            begin = i+1
            handicapInfo.append(False)
        elif (rawframe['id'][i]=='&'):
            dframe.append(rawframe.loc[begin:i-1].reset_index(drop=True))
            begin = i+1
            handicapInfo.append(True)
    dframe.append(rawframe.loc[begin:].reset_index(drop=True))
    dframe.append(rawframe.loc[[]].reset_index(drop=True))
    for df in dframe:
        df['id'] = df['id'].astype(int)
        df['rank'] = df['rank'].astype(float)
    return dframe, handicapInfo

def print_pairing(pairing, dframe, handicapInfo=False):
    pframe = pandas.DataFrame(columns=['Black','White','Handicap','Komi'])
    for i in range(0, len(pairing)/2):
        bindex = pairing[2*i]
        windex = pairing[2*i+1]
        bname = dframe['name'][bindex]
        wname = dframe['name'][windex]
        if (not handicapInfo):
            komi = "7.5"
            handicap = "0"
        else:
            brank = dframe['rank'][bindex]
            wrank = dframe['rank'][windex]
            if (brank > wrank):
                bname, wname = wname, bname
                brank, wrank = wrank, brank
            rdiff = int(wrank-brank)
            if (rdiff == 0):
                komi = "7.5"
                handicap = "0"
            elif (rdiff == 1):
                komi = "0.5"
                handicap = "0"
            else:
                komi = "0.5"
                handicap = str(rdiff)
        pframe.loc[len(pframe)] = [bname,wname,handicap,komi]
    return pframe